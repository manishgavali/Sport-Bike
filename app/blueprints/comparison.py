from flask import Blueprint, render_template, request, jsonify
from app.models.bike import Bike
from app.models.bike_specs import BikeSpec
from app.services.comparison_engine import ComparisonEngine
from app import db

comparison_bp = Blueprint('comparison', __name__)

@comparison_bp.route('/')
def index():
    bikes = Bike.query.filter_by(is_active=True).all()
    return render_template('comparison/select_bikes.html', bikes=bikes)

@comparison_bp.route('/results', methods=['POST'])
def results():
    bike_slugs = request.form.getlist('bike_ids[]')
    
    if len(bike_slugs) < 2:
        return render_template('comparison/select_bikes.html', 
                             error='Please select at least 2 bikes to compare')
    
    # Detailed bike data with all specifications
    bike_data_map = {
        'yamaha-r15-v4': {
            'brand': 'Yamaha', 'model': 'R15 V4', 'price': 197000, 'category': 'Entry',
            'engine_cc': 155, 'engine_type': 'Liquid-cooled, Single-cylinder', 'power': 18.4, 'torque': 14.2,
            'mileage': '45-50', 'weight': 141, 'seat_height': 815, 'gearbox': '6-speed with slipper clutch',
            'features': ['VVA technology', 'Traction Control', 'Quick-shifter (upshift)', 'Dual-channel ABS'],
            'owner_notes': 'Very reliable. Low maintenance. Best for beginners & daily + highway'
        },
        'bajaj-pulsar-rs200': {
            'brand': 'Bajaj', 'model': 'Pulsar RS 200', 'price': 172000, 'category': 'Entry',
            'engine_cc': 199.5, 'engine_type': 'Liquid-cooled', 'power': 24.5, 'torque': 18.5,
            'mileage': '35', 'weight': 166, 'seat_height': 810, 'gearbox': '6-speed',
            'features': ['Triple spark engine', 'Dual-channel ABS', 'Comfortable riding posture'],
            'owner_notes': 'Affordable full-faired bike. Parts easily available. Slight vibration at high RPM'
        },
        'ktm-rc160': {
            'brand': 'KTM', 'model': 'RC 160', 'price': 191000, 'category': 'Entry',
            'engine_cc': 160, 'engine_type': 'Single-cylinder', 'power': 17, 'torque': 14.5,
            'mileage': '40', 'weight': 160, 'seat_height': 820, 'gearbox': '6-speed',
            'features': ['Aggressive KTM design', 'Stiff chassis', 'Track-focused ergonomics'],
            'owner_notes': 'Sporty but not comfortable for city. Maintenance cost medium'
        },
        'hero-xtreme-160r-4v': {
            'brand': 'KTM', 'model': 'RC 125', 'price': 185000, 'category': 'Entry',
            'engine_cc': 124.7, 'engine_type': 'Single-cylinder', 'power': 14.5, 'torque': 12,
            'mileage': '40-45', 'weight': 160, 'seat_height': 820, 'gearbox': '6-speed',
            'features': ['Trellis frame', 'WP suspension'],
            'owner_notes': 'Looks big, power is low. High price for 125 cc'
        },
        'suzuki-gixxer-sf-250': {
            'brand': 'Suzuki', 'model': 'Gixxer SF 250', 'price': 200000, 'category': 'Entry',
            'engine_cc': 249, 'engine_type': 'Oil-cooled', 'power': 26.5, 'torque': 22.6,
            'mileage': '35', 'weight': 161, 'seat_height': 800, 'gearbox': '6-speed',
            'features': ['Strong low-end torque', 'Good highway stability'],
            'owner_notes': 'Best daily + touring sport bike. Low vibration'
        },
        'honda-cbr250r': {
            'brand': 'Suzuki', 'model': 'Gixxer SF 150', 'price': 165000, 'category': 'Entry',
            'engine_cc': 155, 'engine_type': 'Oil-cooled', 'power': 13.6, 'torque': 13.8,
            'mileage': '45', 'weight': 148, 'seat_height': 785, 'gearbox': '5-speed',
            'features': ['Smooth engine', 'Comfortable seating'],
            'owner_notes': 'Very reliable. Low service cost. Less aggressive than R15'
        },
        'yamaha-fz-x': {
            'brand': 'Bajaj', 'model': 'Pulsar NS200', 'price': 148000, 'category': 'Entry',
            'engine_cc': 199.5, 'engine_type': 'Liquid-cooled', 'power': 24.5, 'torque': 18.5,
            'mileage': '35', 'weight': 158, 'seat_height': 805, 'gearbox': '6-speed',
            'features': ['Naked sport', 'Strong performance'],
            'owner_notes': 'Easy to ride. Good spare availability'
        },
        'suzuki-gixxer-250': {
            'brand': 'Keeway', 'model': 'RR 300', 'price': 320000, 'category': 'Entry',
            'engine_cc': 292, 'engine_type': 'Liquid-cooled', 'power': 27.5, 'torque': 25,
            'mileage': '30', 'weight': 165, 'seat_height': 795, 'gearbox': '6-speed',
            'features': ['Sporty design', 'LED lighting'],
            'owner_notes': 'New brand. Service network limited. Looks very sporty'
        },
        'tvs-apache-rr310': {
            'brand': 'TVS', 'model': 'Apache RR 310', 'price': 280000, 'category': 'Performance',
            'engine_cc': 312, 'engine_type': 'Liquid-cooled, Single-cylinder', 'power': 34, 'torque': 27.3,
            'mileage': '30', 'weight': 169, 'seat_height': 810, 'gearbox': '6-speed',
            'features': ['Ride modes', 'TFT display', 'Bi-directional quick-shifter'],
            'owner_notes': 'Best Indian-made track bike. Service quality depends on city'
        },
        'bmw-g310rr': {
            'brand': 'BMW', 'model': 'G 310 RR', 'price': 310000, 'category': 'Performance',
            'engine_cc': 312, 'engine_type': 'Liquid-cooled, Single-cylinder', 'power': 34, 'torque': 28,
            'mileage': '30', 'weight': 164, 'seat_height': 835, 'gearbox': '6-speed',
            'features': ['BMW styling', 'Premium build quality'],
            'owner_notes': 'Premium feel. Service cost higher than TVS'
        },
        'ktm-rc200': {
            'brand': 'KTM', 'model': 'RC 200', 'price': 225000, 'category': 'Performance',
            'engine_cc': 199, 'engine_type': 'Liquid-cooled, Single-cylinder', 'power': 25, 'torque': 19.5,
            'mileage': '35', 'weight': 154, 'seat_height': 820, 'gearbox': '6-speed',
            'features': ['Trellis frame', 'WP suspension', 'Aggressive ergonomics'],
            'owner_notes': 'Hardcore riding position. Fun on track, tiring in city'
        },
        'ktm-rc390': {
            'brand': 'KTM', 'model': 'RC 390', 'price': 310000, 'category': 'Performance',
            'engine_cc': 373, 'engine_type': 'Liquid-cooled, Single-cylinder', 'power': 43, 'torque': 37,
            'mileage': '28', 'weight': 172, 'seat_height': 820, 'gearbox': '6-speed',
            'features': ['Ride-by-wire', 'Cornering ABS', 'TFT display'],
            'owner_notes': 'Very fast. Requires skilled rider. Higher maintenance'
        },
        'kawasaki-ninja300': {
            'brand': 'Kawasaki', 'model': 'Ninja 300', 'price': 350000, 'category': 'Performance',
            'engine_cc': 296, 'engine_type': 'Liquid-cooled, Parallel-twin', 'power': 39, 'torque': 27,
            'mileage': '30', 'weight': 172, 'seat_height': 785, 'gearbox': '6-speed',
            'features': ['Twin-cylinder smoothness', 'Dual-channel ABS', 'Slipper clutch'],
            'owner_notes': 'Smooth engine. Reliable. Expensive spare parts'
        },
        'kawasaki-ninja400': {
            'brand': 'Kawasaki', 'model': 'Ninja 400', 'price': 525000, 'category': 'Performance',
            'engine_cc': 399, 'engine_type': 'Liquid-cooled, Parallel-twin', 'power': 45, 'torque': 38,
            'mileage': '28', 'weight': 168, 'seat_height': 785, 'gearbox': '6-speed',
            'features': ['Lightweight chassis', 'Slipper clutch', 'LED lighting'],
            'owner_notes': 'Lightweight & powerful. Limited availability in India'
        },
        'yamaha-r3': {
            'brand': 'Yamaha', 'model': 'R3', 'price': 450000, 'category': 'Performance',
            'engine_cc': 321, 'engine_type': 'Liquid-cooled, Parallel-twin', 'power': 42, 'torque': 29.5,
            'mileage': '30', 'weight': 169, 'seat_height': 780, 'gearbox': '6-speed',
            'features': ['Twin-cylinder', 'Slipper clutch', 'Dual-channel ABS'],
            'owner_notes': 'Very refined. High price'
        },
        'aprilia-rs457': {
            'brand': 'Aprilia', 'model': 'RS 457', 'price': 415000, 'category': 'Premium',
            'engine_cc': 457, 'engine_type': 'Liquid-cooled, Parallel-twin', 'power': 47.6, 'torque': 43.5,
            'mileage': '28', 'weight': 175, 'seat_height': 800, 'gearbox': '6-speed',
            'features': ['Ride modes', 'TFT display', 'Traction control'],
            'owner_notes': 'Excellent handling. New service network'
        },
        'kawasaki-ninja650': {
            'brand': 'Kawasaki', 'model': 'Ninja 650', 'price': 720000, 'category': 'Premium',
            'engine_cc': 649, 'engine_type': 'Liquid-cooled, Parallel-twin', 'power': 68, 'torque': 65,
            'mileage': '23', 'weight': 196, 'seat_height': 790, 'gearbox': '6-speed',
            'features': ['Comfortable ergonomics', 'Slipper clutch', 'Dual-channel ABS'],
            'owner_notes': 'Comfortable sport touring. Beginner-friendly big bike'
        },
        'honda-cbr650r': {
            'brand': 'Honda', 'model': 'CBR650R', 'price': 950000, 'category': 'Premium',
            'engine_cc': 649, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 95, 'torque': 63,
            'mileage': '20', 'weight': 208, 'seat_height': 810, 'gearbox': '6-speed',
            'features': ['Inline-4 engine', 'Showa suspension', 'LED lighting'],
            'owner_notes': 'Smooth sound. Very reliable. Expensive'
        },
        'aprilia-rs660': {
            'brand': 'Aprilia', 'model': 'RS 660', 'price': 1350000, 'category': 'Premium',
            'engine_cc': 659, 'engine_type': 'Liquid-cooled, Parallel-twin', 'power': 100, 'torque': 67,
            'mileage': '22', 'weight': 183, 'seat_height': 820, 'gearbox': '6-speed',
            'features': ['Advanced electronics', 'Ride modes', 'Cornering ABS', 'Quick-shifter'],
            'owner_notes': 'Advanced electronics. Premium maintenance'
        },
        'kawasaki-zx6r': {
            'brand': 'Kawasaki', 'model': 'Ninja ZX-6R', 'price': 1100000, 'category': 'Premium',
            'engine_cc': 636, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 130, 'torque': 70,
            'mileage': '18', 'weight': 196, 'seat_height': 830, 'gearbox': '6-speed',
            'features': ['High-revving engine', 'Track-focused', 'Quick-shifter'],
            'owner_notes': 'Track weapon. Not city-friendly'
        },
        'suzuki-hayabusa': {
            'brand': 'Suzuki', 'model': 'Hayabusa', 'price': 1680000, 'category': 'Superbike',
            'engine_cc': 1340, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 190, 'torque': 150,
            'mileage': '15', 'weight': 264, 'seat_height': 800, 'gearbox': '6-speed',
            'features': ['Advanced electronics', 'Cruise control', 'Launch control'],
            'owner_notes': 'Heavy. Comfortable superbike. Expensive tyres'
        },
        'kawasaki-zx10r': {
            'brand': 'Kawasaki', 'model': 'Ninja ZX-10R', 'price': 1490000, 'category': 'Superbike',
            'engine_cc': 998, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 203, 'torque': 115,
            'mileage': '14', 'weight': 207, 'seat_height': 835, 'gearbox': '6-speed',
            'features': ['Race-derived electronics', 'Quick-shifter', 'Cornering ABS'],
            'owner_notes': 'Race machine. Needs expert rider'
        },
        'kawasaki-h2': {
            'brand': 'Kawasaki', 'model': 'Ninja H2', 'price': 3650000, 'category': 'Superbike',
            'engine_cc': 998, 'engine_type': 'Supercharged, Inline-4', 'power': 231, 'torque': 141,
            'mileage': '12', 'weight': 238, 'seat_height': 825, 'gearbox': '6-speed',
            'features': ['Supercharged', 'Advanced electronics', 'Aerodynamic winglets'],
            'owner_notes': 'Extremely dangerous. Track only (H2R)'
        },
        'ducati-panigale-v4': {
            'brand': 'Ducati', 'model': 'Panigale V4', 'price': 2850000, 'category': 'Superbike',
            'engine_cc': 1103, 'engine_type': 'Liquid-cooled, V4', 'power': 214, 'torque': 124,
            'mileage': '13', 'weight': 195, 'seat_height': 830, 'gearbox': '6-speed',
            'features': ['V4 engine', 'Cornering ABS', 'Wheelie control', 'Quick-shifter'],
            'owner_notes': 'Very expensive maintenance'
        },
        'ducati-superleggera': {
            'brand': 'Ducati', 'model': 'Superleggera V4', 'price': 10000000, 'category': 'Superbike',
            'engine_cc': 998, 'engine_type': 'Liquid-cooled, V4', 'power': 234, 'torque': 119,
            'mileage': '12', 'weight': 159, 'seat_height': 830, 'gearbox': '6-speed',
            'features': ['Carbon fiber', 'Racing electronics', 'Limited edition'],
            'owner_notes': 'Collector bike. Extremely rare'
        },
        'bmw-s1000rr': {
            'brand': 'BMW', 'model': 'S1000RR', 'price': 2090000, 'category': 'Superbike',
            'engine_cc': 999, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 210, 'torque': 113,
            'mileage': '14', 'weight': 197, 'seat_height': 824, 'gearbox': '6-speed',
            'features': ['Advanced electronics', 'Dynamic traction control', 'Cornering ABS'],
            'owner_notes': 'Best electronics. High service cost'
        },
        'ktm-1290-super-duke-rr': {
            'brand': 'KTM', 'model': '1290 Super Duke RR', 'price': 2295000, 'category': 'Superbike',
            'engine_cc': 1301, 'engine_type': 'Liquid-cooled, V-twin', 'power': 180, 'torque': 140,
            'mileage': '15', 'weight': 189, 'seat_height': 835, 'gearbox': '6-speed',
            'features': ['Massive torque', 'Carbon wheels', 'Advanced electronics'],
            'owner_notes': 'Brutal torque. Naked superbike'
        },
        'honda-cbr1000rr': {
            'brand': 'Honda', 'model': 'CBR1000RR-R Fireblade', 'price': 2850000, 'category': 'Superbike',
            'engine_cc': 1000, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 217, 'torque': 113,
            'mileage': '14', 'weight': 201, 'seat_height': 830, 'gearbox': '6-speed',
            'features': ['Race-derived engine', 'Advanced electronics', 'Aerodynamic design'],
            'owner_notes': 'Legendary reliability'
        },
        'yamaha-r1': {
            'brand': 'Yamaha', 'model': 'YZF-R1', 'price': 2450000, 'category': 'Superbike',
            'engine_cc': 998, 'engine_type': 'Liquid-cooled, Inline-4', 'power': 200, 'torque': 112,
            'mileage': '13', 'weight': 201, 'seat_height': 855, 'gearbox': '6-speed',
            'features': ['Crossplane crankshaft', 'Advanced electronics', 'Quick-shifter'],
            'owner_notes': 'Track focused. Not comfortable for roads'
        },
        'triumph-daytona': {
            'brand': 'Triumph', 'model': 'Daytona 765', 'price': 1400000, 'category': 'Superbike',
            'engine_cc': 765, 'engine_type': 'Liquid-cooled, Inline-3', 'power': 130, 'torque': 80,
            'mileage': '18', 'weight': 189, 'seat_height': 825, 'gearbox': '6-speed',
            'features': ['Triple-cylinder', 'Öhlins suspension', 'Brembo brakes'],
            'owner_notes': 'Race-bred. Limited availability'
        }
    }
    
    # Get selected bikes data
    bikes_info = []
    for slug in bike_slugs:
        if slug in bike_data_map:
            bike = bike_data_map[slug].copy()
            bike['slug'] = slug
            # Calculate derived metrics
            bike['power_to_weight'] = round(bike['power'] / (bike['weight'] / 1000), 2)
            bike['price_per_hp'] = round(bike['price'] / bike['power'], 0)
            bikes_info.append(bike)
    
    if len(bikes_info) < 2:
        return render_template('comparison/select_bikes.html', 
                             error='Could not find the selected bikes')
    
    return render_template('comparison/results.html', bikes=bikes_info)
