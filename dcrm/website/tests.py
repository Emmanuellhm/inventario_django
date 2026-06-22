from django.test import TestCase

class HomeViewTest(TestCase):
    def test_home_uses_home_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Bienvenido a la página principal')
