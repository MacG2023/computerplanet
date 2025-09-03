import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_NAME = "products"
APP_DIR = os.path.join(BASE_DIR, APP_NAME)

# Ensure app directory exists
os.makedirs(APP_DIR, exist_ok=True)
os.makedirs(os.path.join(APP_DIR, "templates", APP_NAME), exist_ok=True)

# Files content
files_content = {
    "forms.py": """from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "product_image", "available"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "product_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
""",

    "views.py": """from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
""",

    "urls.py": """from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
""",

    # Templates
    "templates/products/product_list.html": """{% extends "base.html" %}
{% block title %}Products | Computer Planet{% endblock %}
{% block content %}
<div class="container mt-4">
  <div class="d-flex justify-content-between mb-3">
    <h2>Products</h2>
    <a href="{% url 'product_create' %}" class="btn btn-primary">+ Add Product</a>
  </div>
  <div class="row">
    {% for product in products %}
      <div class="col-md-4">
        <div class="card mb-4 shadow-sm">
          {% if product.product_image %}
          <img src="{{ product.product_image.url }}" class="card-img-top" alt="{{ product.name }}">
          {% endif %}
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description|truncatewords:15 }}</p>
            <p><strong>₹{{ product.price }}</strong></p>
            <a href="{% url 'product_detail' product.pk %}" class="btn btn-sm btn-outline-primary">View</a>
            <a href="{% url 'product_update' product.pk %}" class="btn btn-sm btn-outline-secondary">Edit</a>
            <a href="{% url 'product_delete' product.pk %}" class="btn btn-sm btn-outline-danger">Delete</a>
          </div>
        </div>
      </div>
    {% empty %}
      <p>No products available.</p>
    {% endfor %}
  </div>
</div>
{% endblock %}
""",

    "templates/products/product_detail.html": """{% extends "base.html" %}
{% block title %}{{ object.name }} | Computer Planet{% endblock %}
{% block content %}
<div class="container mt-4">
  <div class="card shadow-sm">
    {% if object.product_image %}
    <img src="{{ object.product_image.url }}" class="card-img-top" alt="{{ object.name }}">
    {% endif %}
    <div class="card-body">
      <h3>{{ object.name }}</h3>
      <p>{{ object.description }}</p>
      <p><strong>Price:</strong> ₹{{ object.price }}</p>
      <p><strong>Category:</strong> {{ object.get_category_display }}</p>
      <p><strong>Available:</strong> {{ object.available|yesno:"Yes,No" }}</p>
      <a href="{% url 'product_update' object.pk %}" class="btn btn-primary">Edit</a>
      <a href="{% url 'product_list' %}" class="btn btn-secondary">Back to Products</a>
    </div>
  </div>
</div>
{% endblock %}
""",

    "templates/products/product_form.html": """{% extends "base.html" %}
{% load widget_tweaks %}
{% block title %}{{ view.object|default:'New Product' }} | Computer Planet{% endblock %}
{% block content %}
<div class="container mt-5">
  <div class="card shadow-sm">
    <div class="card-body">
      <h3>{{ view.object|default:"Add Product" }}</h3>
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {% for field in form %}
          <div class="mb-3">
            <label class="form-label">{{ field.label }}</label>
            {{ field|add_class:"form-control" }}
            {% if field.help_text %}
              <small class="form-text text-muted">{{ field.help_text }}</small>
            {% endif %}
            {% for error in field.errors %}
              <div class="text-danger">{{ error }}</div>
            {% endfor %}
          </div>
        {% endfor %}
        <button type="submit" class="btn btn-success">Save</button>
        <a href="{% url 'product_list' %}" class="btn btn-secondary">Cancel</a>
      </form>
    </div>
  </div>
</div>
{% endblock %}
""",

    "templates/products/product_confirm_delete.html": """{% extends "base.html" %}
{% block title %}Delete Product | Computer Planet{% endblock %}
{% block content %}
<div class="container mt-5">
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title">Confirm Delete</h5>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete <strong>{{ object.name }}</strong>?</p>
        </div>
        <div class="modal-footer">
          <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Yes, Delete</button>
            <a href="{% url 'product_list' %}" class="btn btn-secondary">Cancel</a>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
""",
}

# Write files
for filepath, content in files_content.items():
    full_path = os.path.join(APP_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ {APP_NAME} app files generated successfully!")
