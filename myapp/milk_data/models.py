from django.db import models
from django.utils import timezone

# This model stores different cow breeds and their expected milk quality.
class Breed(models.Model):
    """
    Represents a breed of cow.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the cow breed")
    expected_milk_quality = models.IntegerField(help_text="Description of the typical milk quality from this breed.")

    def __str__(self):
        string = f"{self.name} - {self.expected_milk_quality} ltrs/day"
        return string

# This model is for geographical districts. It's linked to the Supplier.
class District(models.Model):
    """
    Represents a geographical district where suppliers are located.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# This is the main table for milk suppliers (farmers).
class Supplier(models.Model):
    """
    Represents a milk supplier or farmer.
    """


    farmer_photo = models.ImageField(upload_to='farmer_photos/', blank=True, null=True)
    name = models.CharField(max_length=150)
    rf_no = models.CharField(max_length=50, unique=True, help_text="Registration or Reference number for the farmer")
    phone_no = models.CharField(max_length=15)
    # Foreign Key to the District table. If a district is deleted, this field becomes null.
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    total_cows = models.PositiveIntegerField(default=0)
    
    # This field tracks the overall quality warning level for the supplier.
    warning_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.rf_no})"

# This table stores information about each individual cow.
class Cow(models.Model):
    """
    Represents an individual cow belonging to a supplier.
    """
    cow_photo = models.ImageField(upload_to='cow_photos/', blank=True, null=True)
    cow_name = models.CharField(max_length=100, help_text="A unique name or ID for the cow")
    # Foreign Key to the Supplier. If a supplier is deleted, all their cows are also deleted.
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="cows")
    # Foreign Key to the Breed.
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    last_vaccination_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.cow_name} (Supplier: {self.supplier.name})"

# This table logs each milk submission from a supplier.
class MilkSubmission(models.Model):
    """
    Represents a single milk quality submission from a supplier.
    """
    # Choices for the quality of a single milk submission


    # Foreign Key to the Supplier.
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="submissions")
    quality_of_milk = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Submission from {self.supplier.name} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

