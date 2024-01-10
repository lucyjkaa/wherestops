from django.shortcuts import render
from django.http import HttpResponse
from .forms import FuelCalculationForm

# Funkcja calculate_distance z uwzględnieniem dodatkowych wyborów
def calculate_distance(route_choice, selected_additional_stops):
    distances = {'1': 360, '2': 370, '3': 410}
    additional_distance = len(selected_additional_stops) * 50
    total_distance = distances.get(route_choice, 0) + additional_distance
    return total_distance

# Funkcje do obliczeń
def calculate_fuel_needed(distance, fuel_consumption):
    return (distance / 100) * fuel_consumption

def calculate_refueling_count(fuel_needed, tank_capacity):
    return fuel_needed / tank_capacity + 1

# Widok Django
def fuel_calculation(request):
    form = FuelCalculationForm()
    selected_stops = []

    if request.method == 'POST':
        form = FuelCalculationForm(request.POST)

        if form.is_valid():
            selected_stops = form.set_stops_choices()

            vehicle_type = form.cleaned_data['vehicle_type']
            route_choice = form.cleaned_data['route_choice']

            if vehicle_type == 'TIR':
                fuel_consumption = 30
                tank_capacity = 600
            elif vehicle_type == 'Samochod dostawczy':
                fuel_consumption = 10
                tank_capacity = 100
            else:
                return HttpResponse("Niepoprawny rodzaj pojazdu.")

            selected_additional_stops = request.POST.getlist('stop')

            distance = calculate_distance(route_choice, selected_additional_stops)
            fuel_needed = calculate_fuel_needed(distance, fuel_consumption)
            refueling_count = calculate_refueling_count(fuel_needed, tank_capacity)

            return render(request, 'result.html', {
                'form': form,
                'selected_stops': selected_stops,
                'fuel_needed': fuel_needed,
                'refueling_count': refueling_count,
                'selected_additional_stops': selected_additional_stops,
                'total_distance': distance,  # Przekazujemy całkowitą trasę do szablonu
            })

    return render(request, 'index.html', {'form': form, 'selected_stops': selected_stops})






