from django.shortcuts import render , get_object_or_404, redirect
from .models import Pengguna, Content  # Impor model Pengguna
from .forms import PenggunaForm, AddressForm , ContentForm
from django.http import JsonResponse
from data_entry.models import Pengguna

# Create your views here.
def set_data_entry(request):
    form = AddressForm()
    context = {
        'form': form,
    }
    return render(request, 'data_entry/input_data.html', context)

# Saat input pengguna, simpan ke session
def set_pengguna(request):
    if request.method == 'POST':
        form = PenggunaForm(request.POST)
        if form.is_valid():
            pengguna = form.save()
            request.session['pengguna_id'] = pengguna.id
            return redirect('data_entry:set_content')
    else:
        form = PenggunaForm()
    return render(request, 'data_entry/pengguna.html', {'form': form})

def view_pengguna(request, id):
    try: 
        pengguna = Pengguna.objects.get(pk=id)  # Perbaiki nama model dan cara mengakses pk
        return render(request, 'data_entry/pengguna_detail.html', {'user_id': id})
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)  

def get_pengguna_detail_api(request, id):
    print(f"Debugging: Mencari pengguna dengan ID {id}")  # Cek apakah ID masuk ke fungsi

    pengguna = get_object_or_404(Pengguna, pk=id)

    data = {
        'email': pengguna.email,
        'address_1': pengguna.address_1,
        'address_2': pengguna.address_2 if pengguna.address_2 else '',
        'city': pengguna.city,
        'state': pengguna.state,
        'zip_code': pengguna.zip_code,
        'tanggal_join': pengguna.tanggal_join.strftime('%Y-%m-%d') if pengguna.tanggal_join else ''
    }

    return JsonResponse(data)
def edit_pengguna(request, id):
    return render(request, 'data_entry/edit_pengguna.html')


# Menampilkan detail pengguna
def user_detail(request, user_id):
    pengguna = get_object_or_404(Pengguna, id=user_id)  # Gunakan 'Pengguna' sesuai model
    return render(request, 'data_entry/user_detail.html', {'pengguna': pengguna})

def search_pengguna_by_state(request):
    state = request.GET.get('state')
    if state:
        pengguna = Pengguna.objects.filter(state__icontains=state)
        return render(request, 'data_entry/search_result.html', {'pengguna': pengguna, 'state': state})
    else:
        return render(request, 'data_entry/search_result.html', {'error': 'Silakan masukkan nama state untuk pencarian.'})

def set_content(request):
    pengguna = None
    pengguna_id = request.session.get('pengguna_id')

    if pengguna_id:
        pengguna = Pengguna.objects.filter(id=pengguna_id).first()

    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_content')
    else:
        # Auto-set author ke pengguna yg login (kalau ada)
        form = ContentForm(initial={'author': pengguna})

    konten_list = Content.objects.all()
    return render(request, 'data_entry/content.html', {
        'form': form,
        'konten_list': konten_list,
        'pengguna': pengguna,
    })

def view_konten(request, id):
    konten = get_object_or_404(Content, pk=id)
    return render(request, 'data_entry/view_konten.html', {'konten': konten})

def edit_konten(request, id):
    konten = get_object_or_404(Content, id=id)

    if request.method == 'POST':
        form = ContentForm(request.POST, instance=konten)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_content')
    else:
        form = ContentForm(instance=konten)

    return render(request, 'data_entry/edit_konten.html', {
        'form': form,
        'konten': konten,
    })