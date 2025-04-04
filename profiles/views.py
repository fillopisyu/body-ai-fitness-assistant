# profiles/views.py
from django.shortcuts import render, redirect, get_object_or_404
# Django'nun hazır formları, mesajlaşma sistemi ve login decorator'ı
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Kendi oluşturduğumuz formlar
from .forms import UserProfileForm

# Yapay zeka, ayarlar ve Markdown için importlar
from django.conf import settings
import google.generativeai as genai
import logging
import markdown2

# API view ve modeller için importlar
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # Geçici
from .models import Conversation, Message, UserProfile, SavedProgram  # Modeller
from django.utils.html import strip_tags  # Başlık için

# Loglama ayarı
logger = logging.getLogger(__name__)


# --- TÜM VIEW FONKSİYONLARI ---

def home_view(request):
    # Ana sayfa görünümü
    return render(request, 'profiles/home.html')


def signup_view(request):
    # Kayıt (Signup) view'ı
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesap başarıyla oluşturuldu: {username}! Artık giriş yapabilirsiniz.')
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'profiles/signup.html', context)


# *** PROFILE_VIEW FONKSİYONU DÜZELTİLDİ (SYNTAXERROR İÇİN) ***
@login_required
def profile_view(request):
    # Kullanıcının profilini bulmaya çalış
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None  # Profil henüz yok

    if request.method == 'POST':
        # POST isteği geldiyse formu işle
        # Eğer profil varsa instance olarak ver (güncelleme için), yoksa verme (yeni oluşturma için)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Form geçerliyse, veritabanına kaydetmeden önce objeyi al
            saved_profile = form.save(commit=False)
            is_new_profile = False  # Yeni mi eski mi olduğunu takip edelim

            if profile is None:  # Eğer bu yeni bir profilse (instance=None ile form oluşturulduysa)
                saved_profile.user = request.user  # Kullanıcıyı ata
                is_new_profile = True

            # Şimdi objeyi veritabanına kaydet (yeni veya güncellenmiş)
            saved_profile.save()

            # Başarı mesajını ayarla
            message_text = "oluşturuldu" if is_new_profile else "güncellendi"
            messages.success(request, f'Profil başarıyla {message_text}!')

            # Profil sayfasına geri yönlendir
            return redirect('profile')
        # else: Form geçerli değilse, sayfa aşağıda hatalı formla tekrar render edilecek
        #      (messages framework veya form.errors şablonda gösterilebilir)

    else:  # GET isteği ise
        # Profili varsa formu doldur, yoksa boş form oluştur
        form = UserProfileForm(instance=profile)

    # Şablonu render et
    context = {
        'form': form,
        'title': 'Profilim' if profile else 'Profil Oluştur'  # Başlığı duruma göre ayarla
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def generate_workout_view(request):
    # Bu view artık kullanılmıyor, yerine API view'ı var. 404 döndürelim.
    from django.http import Http404
    raise Http404("Plan oluşturma API'si /api/generate-plan/ adresindedir.")


@login_required
def chat_page_view(request):
    # Chat sayfasını gösteren ve geçmişi yükleyen view
    conversation = Conversation.objects.filter(user=request.user).order_by('-created_at').first()
    messages_queryset = conversation.messages.all().order_by('timestamp') if conversation else []
    context = {'conversation': conversation, 'messages': messages_queryset, 'title': 'AI Asistan ile Sohbet'}
    return render(request, 'profiles/chat.html', context)


@csrf_exempt  # Geçici
@login_required
@require_POST
def chat_api_view(request):
    # Chat API (hafızalı, sistem talimatlı)
    try:
        try:
            data = json.loads(request.body); user_message_content = data.get('message', '').strip()
        except json.JSONDecodeError:
            user_message_content = request.POST.get('message', '').strip()
        if not user_message_content: return JsonResponse({'success': False, 'error': 'Mesaj boş.'}, status=400)
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profil yok.'}, status=400)

        ai_response_text = "Yanıt alınamadı."
        conversation, created = Conversation.objects.get_or_create(user=request.user)
        Message.objects.create(conversation=conversation, role='user', content=user_message_content)

        # Hafıza kısmı...
        history_limit = 10
        messages_history_qs = conversation.messages.all().order_by('-timestamp')[:history_limit];
        messages_history_qs = reversed(messages_history_qs)
        system_instruction = """Sen 'Ben Body AI'... (önceki talimat)..."""  # Tam talimat metni burada olmalı
        gemini_history = [{"role": "user", "parts": [{"text": system_instruction}]},
                          {"role": "model", "parts": [{"text": "Anladım..."}]}]
        last_user_msg_id = Message.objects.filter(conversation=conversation, role='user').last().id
        for msg in messages_history_qs:
            if msg.role == 'user' and msg.id == last_user_msg_id: continue
            if msg.content and msg.role in ['user', 'model']: gemini_history.append(
                {"role": msg.role, "parts": [{"text": msg.content}]})

        # API Çağrısı...
        try:
            gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None);
            assert gemini_api_key, "API key yok."
            genai.configure(api_key=gemini_api_key);
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(user_message_content);
            ai_response_text = response.text
        except Exception as e:
            logger.error(f"Gemini hatası: {e}", exc_info=True); ai_response_text = f"Sorun: {e}"

        Message.objects.create(conversation=conversation, role='model', content=ai_response_text)
        return JsonResponse({'success': True, 'response': ai_response_text, 'error': None})
    except Exception as e:
        logger.error(f"Chat API hatası: {e}", exc_info=True); return JsonResponse(
            {'success': False, 'error': 'Sunucu hatası'}, status=500)


@login_required
def generate_plan_api_view(request):
    # Plan Oluşturma API view (POST kabul eder, özel istek alır)
    if request.method == 'POST':
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': "Profil bulunamadı."}, status=404)
        if not all([profile.goal, profile.age, profile.weight_kg, profile.height_cm]): return JsonResponse(
            {'success': False, 'error': 'Profil bilgilerinizi tamamlayın.', 'redirect_to_profile': True}, status=400)
        custom_request_text = "";
        workout_plan_html = None;
        error_message = None;
        workout_plan_text_raw = None
        try:
            data = json.loads(request.body); custom_request_text = data.get('custom_request', '').strip()
        except Exception as e:
            logger.warning(f"Özel istek alınamadı: {e}")
        try:
            gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None);
            assert gemini_api_key, "API key bulunamadı."
            genai.configure(api_key=gemini_api_key);
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Prompt (Özel istek dahil)
            prompt = f"""Kullanıcı Profili: Yaş: {profile.age}... Hedef: {profile.get_goal_display()}. Kullanıcının Özel İsteği: {custom_request_text if custom_request_text else "Yok"}. Görev: ... Lütfen cevabı Markdown formatında ver... EGZERSİZ_LISTESI_BASLANGIC..."""  # Tam prompt metni önceki yanıtlarda var
            response = model.generate_content(prompt);
            workout_plan_text_raw = response.text
            workout_plan_html = markdown2.markdown(workout_plan_text_raw,
                                                   extras=["tables", "fenced-code-blocks", "strike",
                                                           "break-on-newline"])
            return JsonResponse({'success': True, 'plan_html': workout_plan_html, 'plan_text': workout_plan_text_raw})
        except Exception as e:
            logger.error(f"Plan API hatası: {e}", exc_info=True); return JsonResponse(
                {'success': False, 'error': f"Plan oluşturulamadı: {e}"}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Sadece POST istekleri desteklenmektedir.'}, status=405)


# *** PROGRAM KAYDETME VIEW'I (BAŞLIK ÇIKARMA DÜZELTİLDİ) ***
@login_required
@require_POST
def save_program_view(request):
    # Formdan gelen verileri al
    # Dikkat: workout_plan.html'deki formda name='program_text' kullandık
    program_raw_text = request.POST.get('program_text')
    program_title_input = request.POST.get('program_title', None)

    if program_raw_text:
        # Önce HTML içeriğini oluşturalım (veritabanına bunu kaydedeceğiz)
        program_html_content = markdown2.markdown(
            program_raw_text,
            extras=["tables", "fenced-code-blocks", "strike", "break-on-newline"]
        )

        program_title = program_title_input # Kullanıcı başlık girdiyse onu kullan
        extracted_exercises = ""

        # Kullanıcı başlık girmediyse içerikten çıkarmayı dene
        if not program_title:
             try:
                 # İçerikteki ilk H2 etiketini bulup başlık yapmayı dene
                 # Not: Bu yöntem basit ve her zaman çalışmayabilir.
                 # Daha sağlam yöntem için BeautifulSoup gibi HTML parser kütüphaneleri gerekir.
                 start_tag = '<h2'
                 end_tag = '</h2'
                 start_index = program_html_content.find(start_tag)
                 if start_index != -1:
                     # H2 etiketinin içeriğini al
                     content_start = program_html_content.find('>', start_index) + 1
                     content_end = program_html_content.find(end_tag, content_start)
                     if content_end != -1:
                         temp_title = program_html_content[content_start:content_end]
                         program_title = strip_tags(temp_title).strip()[:190] # HTML etiketlerini temizle, kısalt
                     else:
                          program_title = "Kaydedilen Plan" # H2 içeriği bulunamazsa
                 else:
                     program_title = "Kaydedilen Plan" # H2 etiketi hiç yoksa
             except Exception:
                 # Herhangi bir hata olursa varsayılan başlığı kullan
                 program_title = "Kaydedilen Plan"

        # Egzersiz listesini ayrıştır (önceki kod)
        try:
            start_marker="EGZERSİZ_LISTESI_BASLANGIC"; end_marker="EGZERSİZ_LISTESI_BITIS"
            start_index=program_raw_text.find(start_marker); end_index=program_raw_text.find(end_marker)
            if start_index != -1 and end_index != -1:
                exercise_block=program_raw_text[start_index+len(start_marker):end_index]
                lines=[line.strip() for line in exercise_block.splitlines() if line.strip().startswith('*')]
                extracted_exercises="\n".join([line.lstrip('*').strip() for line in lines])
        except Exception as ex:
            logger.warning(f"Egzersiz listesi ayrıştırılamadı: {ex}")

        # Veritabanına kaydet
        try:
            SavedProgram.objects.create(
                user=request.user,
                content_html=program_html_content, # Oluşturulan HTML'i kaydet
                title=program_title,
                exercise_list=extracted_exercises # Ayrıştırılan listeyi kaydet
            )
            messages.success(request, f"'{program_title}' başarıyla kaydedildi!")
            return redirect('my_programs') # Programlarım sayfasına yönlendir
        except Exception as e:
            logger.error(f"Program kaydetme hatası: {e}", exc_info=True)
            messages.error(request, "Program kaydedilirken bir hata oluştu.")
    else:
        messages.warning(request, "Kaydedilecek program içeriği bulunamadı.")

    # Hata durumunda veya içerik yoksa profile geri dön
    # Veya planın oluşturulduğu sayfaya geri dönebiliriz, ama o sayfa state tutmuyor.
    # Profile dönmek daha güvenli.
    return redirect('profile')

@login_required
def my_programs_view(request):
    # Kaydedilen Programları Listeleme
    saved_programs = SavedProgram.objects.filter(user=request.user).order_by('-created_at')
    context = {'saved_programs': saved_programs, 'title': 'Kaydedilen Programlarım'}
    return render(request, 'profiles/my_programs.html', context)


@login_required
@ require_POST
def delete_program_view(request, program_id):
    # Program Silme
    program = get_object_or_404(SavedProgram, pk=program_id, user=request.user)
    try:
        title = program.title or "Başlıksız"; program.delete(); messages.success(request, f"'{title}' silindi.")
    except Exception as e:
        logger.error(f"Silme hatası: {e}", exc_info=True); messages.error(request, "Silinirken hata.")
    return redirect('my_programs')


@login_required
@ require_POST
def toggle_program_status_view(request, program_id):
    # Tamamlanma Durumunu Değiştirme
    program = get_object_or_404(SavedProgram, pk=program_id, user=request.user)
    try:
        program.completed = not program.completed; program.save(); status = "Tamamlandı" if program.completed else "Tamamlanmadı"; messages.info(
            request, f"'{program.title or 'Program'}' durumu '{status}' güncellendi.")
    except Exception as e:
        logger.error(f"Durum hatası: {e}", exc_info=True); messages.error(request, "Durum değiştirilemedi.")
    return redirect('my_programs')


@login_required
def dashboard_view(request):
    # Kontrol Paneli
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.warning(request, "Lütfen profili tamamlayın."); return redirect('profile')
    saved = SavedProgram.objects.filter(user=request.user)
    context = {'profile': profile, 'saved_programs_count': saved.count(),
               'completed_programs_count': saved.filter(completed=True).count(),
               'conversation_count': Conversation.objects.filter(user=request.user).count(), 'title': 'Kontrol Paneli'}
    return render(request, 'profiles/dashboard.html', context)


@login_required
@require_POST
def clear_chat_history_view(request):
    try:
        conversation = Conversation.objects.filter(user=request.user).order_by('-created_at').first()
        if conversation:
            conversation.messages.all().delete()
            messages.success(request, "Sohbet geçmişi başarıyla temizlendi.")
        else:
            messages.info(request, "Temizlenecek sohbet geçmişi bulunamadı.")
    except Exception as e:
        logger.error(f"Sohbet temizleme hatası: {e}", exc_info=True)
        messages.error(request, "Sohbet geçmişi temizlenirken bir hata oluştu.")
    return redirect('chat_page')