from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.sabores_da_terra.security import get_current_user

router = APIRouter()
template = Jinja2Templates(directory='src/sabores_da_terra/templates')


@router.get('/', response_class=HTMLResponse)
async def home(
    request: Request,
    user=Depends(get_current_user),

):
    return template.TemplateResponse(
        'index.html', {'request': request, 'user': user})


@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return template.TemplateResponse('register.html', {'request': request})


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return template.TemplateResponse('login.html', {'request': request})


@router.get('/cart', response_class=HTMLResponse)
async def cart(request: Request, user=Depends(get_current_user)):
    return template.TemplateResponse(
        'cart.html', {'request': request, 'user': user}
    )


@router.get('/product-page/{product_id}', response_class=HTMLResponse)
async def product_page(
    product_id: int, request: Request, user=Depends(get_current_user)
):
    return template.TemplateResponse(
        'product.html',
        {'request': request, 'product_id': product_id, 'user': user},
    )


@router.get('/perfil', response_class=HTMLResponse)
async def get_perfil(request: Request, user=Depends(get_current_user)):
    return template.TemplateResponse(
        'perfil.html', {'request': request, 'user': user}
    )


@router.get('/admin-panel', response_class=HTMLResponse)
async def admin_panel(request: Request, user=Depends(get_current_user)):
    return template.TemplateResponse(
        'admin.html', {'request': request, 'user': user}
    )


@router.get('/payment-success', response_class=HTMLResponse)
async def payment_success(request: Request):
    return template.TemplateResponse(
        'payment_success.html', {'request': request}
    )


@router.get('/payment-failure', response_class=HTMLResponse)
async def payment_failure(request: Request):
    return template.TemplateResponse(
        'payment_failure.html', {'request': request}
    )
