from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property, InterestedBuyer
from .forms import PropertyForm # type: ignore
from django.core.paginator import Paginator
from django_filters import rest_framework as filters
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Property

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form})

@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})

@login_required
def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/property_form.html', {'form': form})

@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('property_list')
    return render(request, 'properties/property_confirm_delete.html', {'property': property})

@login_required
def interested_in_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    seller_email = property.seller.email
    buyer_email = request.user.email

    # Send email to seller
    send_mail(
        subject=f'Interest in your property: {property.title}',
        message=f'Hello {property.seller.first_name},\n\n'
                f'{request.user.first_name} {request.user.last_name} is interested in your property "{property.title}".\n'
                f'You can contact them at {buyer_email}.\n\n'
                f'Best regards,\nRentify Team',
        from_email='no-reply@example.com',
        recipient_list=[seller_email],
    )

    # Send email to buyer
    send_mail(
        subject=f'Interest in property: {property.title}',
        message=f'Hello {request.user.first_name},\n\n'
                f'You have expressed interest in the property "{property.title}".\n'
                f'The seller is {property.seller.first_name} {property.seller.last_name} and can be contacted at {seller_email}.\n\n'
                f'Best regards,\nRentify Team',
        from_email='no-reply@example.com',
        recipient_list=[buyer_email],
    )

    return HttpResponse('An email has been sent to the seller and you have been notified.')

@login_required
def like_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.user in property.likes.all():
        property.likes.remove(request.user)
    else:
        property.likes.add(request.user)
    return redirect('property_detail', pk=pk)
class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = ['place', 'area', 'bedrooms', 'bathrooms', 'price']

def property_list(request):
    property_list = Property.objects.all()
    property_filter = PropertyFilter(request.GET, queryset=property_list)
    paginator = Paginator(property_filter.qs, 10)  # Show 10 properties per page.
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    return render(request, 'properties/property_list.html', {'properties': properties, 'filter': property_filter})