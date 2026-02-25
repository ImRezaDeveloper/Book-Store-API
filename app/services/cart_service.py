from fastapi_redis_cache import FastApiRedisCache
cache = FastApiRedisCache()

class CartService:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        
        if self.user:
            self.key = f'cart_user{self.user}'
        else:
            if not request.session.session_key:
                request.session.create()
            self.key = f"cart_session_{request.session.session_key}"
    
    async def get_cart(self):
        cart = cache.get_cache_key(self.key, {})
        return await cart
    
    def add_cart(self, product_id:int, quantity: int):
        product_id = str(product_id)
        cart = self.get_cart()
        
        if product_id in cart:
            cart[product_id]["quantity"] += 1
        else:
            cart[product_id] = {"quantity": quantity}
        
        cache.add_to_cache(key=self.key, value=cart, expire=86400)
        
    def remove_cart(self, product_id:int, quantity: int):
        product_id = str(product_id)
        cart = self.get_cart()
        
        if product_id in cart:
            cart[product_id]["quantity"] -= 1
        else:
            if cart[product_id]["quantity"] <= 0:
                del cart[product_id]
                
        cache.add_to_cache(key=self.key, value=cart, expire=86400)
    
    def clear_cart(self):
        cache.add_to_cache(key=self.key, value={}, expire=86400)