from django.contrib import admin
from django.test import TestCase, override_settings

from .admin import site
from .models import Cat, CatFood, Dog, DogFood


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, module):
        return True


request = MockRequest()
request.user = MockSuperUser()


DEFAULT_APP = 'admin_grouping'

CAT_APP = 'cats'
DOG_APP = 'dogs'


@override_settings(ROOT_URLCONF='admin_grouping.urls')
class TestAdminGrouping(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cat = Cat.objects.create(name="Fluffy")
        cls.dog = Dog.objects.create(name="Rex")
        cls.cat_food = CatFood.objects.create(name="Fluffy's can of Tuna")
        cls.dog_food = DogFood.objects.create(name="Rex's biscuits")

    def default_set_up(self):
        site.register(Cat)
        site.register(CatFood)
        site.register(Dog)
        site.register(DogFood)

    def custom_set_up(self):
        """
        In the custom case we will prepare some special group_names for all models in the admin.
        """
        class CatAdmin(admin.ModelAdmin):
            group_name = CAT_APP

        class DogAdmin(admin.ModelAdmin):
            group_name = DOG_APP

        site.register(Cat, CatAdmin)
        site.register(CatFood, CatAdmin)
        site.register(Dog, DogAdmin)
        site.register(DogFood, DogAdmin)

    def _get_models_from_app_dict_entry(self, app_dict_entry):
        """
        Helper to get a flat list of models within an entry in app_dict.
        """
        return list(map(lambda s: s['model'], app_dict_entry['models']))

    def tearDown(self):
        site.unregister(Cat)
        site.unregister(CatFood)
        site.unregister(Dog)
        site.unregister(DogFood)

    def test_default_grouping(self):
        self.default_set_up()
        app_dict = site._build_app_dict(request)

        self.assertIn(DEFAULT_APP, app_dict)

        default_models = self._get_models_from_app_dict_entry(app_dict[DEFAULT_APP])

        self.assertIn(Cat, default_models)
        self.assertIn(Dog, default_models)
        self.assertIn(CatFood, default_models)
        self.assertIn(DogFood, default_models)

    def test_custom_grouping(self):
        self.custom_set_up()
        app_dict = site._build_app_dict(request)

        self.assertIn(CAT_APP, app_dict)
        self.assertIn(DOG_APP, app_dict)

        cat_models = self._get_models_from_app_dict_entry(app_dict[CAT_APP])
        dog_models = self._get_models_from_app_dict_entry(app_dict[DOG_APP])

        self.assertIn(Cat, cat_models)
        self.assertIn(Dog, dog_models)
        self.assertIn(CatFood, cat_models)
        self.assertIn(DogFood, dog_models)
