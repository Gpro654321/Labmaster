from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class NeverCacheMixin:
    '''
    A custom mixin to prevent auto caching of pages by calling the 
    dispatch method
    '''
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        print("I am inside NeverCacheMixin")
        return super().dispatch(request, *args, **kwargs)

