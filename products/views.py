from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg

from .models import Product, Category, Review
from checkout.models import Order
from .forms import ReviewForm, ProductForm


class ProductListView(ListView):
    """A Class Based View to show all products, including search queries,
    to check average product rating and save it to DB if changed"""
    model = Product    
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        for product in Product.objects.all():        
            approved_reviews = Review.objects.filter(
                product_id=product.id, approved=True)
            avg = approved_reviews.aggregate(Avg('rate'))['rate__avg']
            if avg is not None:
                rounded_avg = 0.5 * round(avg/0.5)
                if product.rating != rounded_avg:
                    product.rating = rounded_avg
                    product.save()
            else:
                product.rating = None
                product.save()
        response = super().get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset(
                   ).order_by('name')
        q = self.request.GET.get('q')
        if q:
            queryset = self.model.objects.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
                )
        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['q'] = self.request.GET.get('q')
        return context


def CategoryView(request, slug):
    """A view to get all product categories and
    products by current category
    """
    try:
        current_category = Category.objects.get(name=slug)
        category_products = Product.objects.filter(
            category=current_category).order_by('name')
        all_categories = Category.objects.all()
        context = {
            'category_products': category_products,
            'slug': slug,
            'categories': all_categories
        }
        return render(request, 'products/products.html', context)
    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist")
        return redirect('products:products')


def product_detail(request, product_id):
    """A view to show individual product details"""
    product = get_object_or_404(Product, pk=product_id)
    category = Category.objects.filter(product=product)
    reviews = Review.objects.filter(
            product_id=product.id, approved=True)
    context = {
        "product": product,
        "category": category,
        "reviews": reviews,
    }
    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('core'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request,
                             'Successfully added product!',
                             extra_tags='flag')
            return redirect(reverse(
                'products:product_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to add product. '
                           'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('core'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Successfully updated product!',
                             extra_tags='flag')
            return redirect(reverse(
                'products:product_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to update product. '
                           'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('core'))
    product = get_object_or_404(Product, pk=product_id)
    delete_product = request.GET.get('delete_product')
    if product:
        if delete_product:
            product.delete()
            messages.success(request, 'Product deleted!', extra_tags='flag')
            return redirect('products:products')
        else:
            template = 'products/delete_product.html'
            context = {
                'product': product,
                'flag': True,
            }
            return render(request, template, context)
    else:
        messages.error(request,
                       'Sorry, product not exists.')
        return redirect(reverse('products:products'))


class ReviewView(SuccessMessageMixin, CreateView):
    """A Class Based View to get product review from
    the user and redirect him to order history page
    """
    model = Review
    form_class = ReviewForm
    template_name = 'products/review_product.html'
    success_url = '/order_details/'

    def get_success_url(self):
        return reverse('profile:order_details', kwargs={
                       'order_id': self.kwargs['order_id']})

    def form_valid(self, form):
        form.instance.user = self.request.user.userprofile
        form.instance.product_id = self.kwargs['product_id']
        success_message = ("Thank you for the review! "
                           "It will be published after admin approval.")
        extra_tags = 'flag'
        messages.success(self.request, success_message, extra_tags=extra_tags)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(
            Product, pk=self.kwargs['product_id'])
        context['order_id'] = get_object_or_404(
            Order, user_profile=self.request.user.userprofile,
            id=self.kwargs['order_id'])
        return context


@login_required
def show_reviews(request):
    """ Display all not approved reviews to admin """
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store owners can access this page.')
        return redirect(reverse('core'))
    reviews = Review.objects.filter(approved=False)
    template = 'products/show_reviews.html'
    context = {
        'reviews': reviews,
    }
    return render(request, template, context)


@login_required
def approve_review(request, product_id, review_id):
    """ View to approve review by admin and  
    to calculate average product rating"""
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store owners can access this page.')
        return redirect(reverse('core'))
    r_to_approve = Review.objects.get(product_id=product_id, id=review_id)
    r_to_approve.approved = True
    r_to_approve.save()
    """ Calculate and save to DB average product rating"""
    product = Product.objects.get(pk=product_id)
    approved_reviews = Review.objects.filter(
        product_id=product_id, approved=True)
    avg = approved_reviews.aggregate(Avg('rate'))['rate__avg']
    rounded_avg = 0.5 * round(avg/0.5)
    product.rating = rounded_avg
    product.save()
    return redirect('products:show_reviews')
