from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import timedelta
from dashboard.models import Post, Program, Faculty, Facility, AcademicCalendar, Announcement, Alumni, News, Achievement, College, MediaUpload, AlumniAbout, AlumniNews, AlumniEvent, AlumniSuccessStory


def _safe_int(value, default=0):
    if value is None:
        return default
    if isinstance(value, str) and value.strip() == '':
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def index(request):
    # Get latest published posts for the homepage
    # FILTER: Only show Superadmin posts (college='all') in "Latest at NORSU"
    posts = Post.objects.filter(status='published', college='all').order_by('-created_at')[:6]
    
    # Get achievements for the homepage
    achievements = Achievement.objects.filter(status='published').order_by('-created_at')
    
    # Get alumni success stories for the homepage
    success_stories = AlumniSuccessStory.objects.filter(status='published').order_by('-created_at')[:3]
    
    # Add is_new flag to each post (posts created within last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    for post in posts:
        post.is_new = post.created_at >= seven_days_ago

    college_totals = College.objects.aggregate(
        total_students=Sum('total_students'),
        total_instructors=Sum('qualified_instructors'),
        total_programs=Sum('programs_offered'),
    )
    total_colleges = College.objects.count()

    context = {
        'posts': posts,
        'achievements': achievements,
        'success_stories': success_stories,
        'total_colleges': total_colleges,
        'total_students': college_totals.get('total_students') or 0,
        'total_instructors': college_totals.get('total_instructors') or 0,
        'total_programs': college_totals.get('total_programs') or 0,
    }
    
    return render(request, 'dashboard/index.html', context)

def admin_login(request):
    return render(request, 'dashboard/admin-login.html')

@login_required(login_url='/super-admin-login/')
def admin_dashboard(request):
    return render(request, 'dashboard/admin-dashboard.html')

@csrf_exempt
def super_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/super-admin-dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'dashboard/super-admin-login.html')

@login_required(login_url='/super-admin-login/')
def super_admin_dashboard(request):
    return render(request, 'dashboard/super-admin-dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('/')

def cas_dashboard(request):
    return render(request, 'dashboard/dashbordcas.html')

def cit_dashboard(request):
    return render(request, 'dashboard/dashbordcit.html')

def caf_dashboard(request):
    return render(request, 'dashboard/dashbordcaf.html')

def cted_dashboard(request):
    return render(request, 'dashboard/dashbordcted.html')

def ccje_dashboard(request):
    return render(request, 'dashboard/dashbordccje.html')

def cba_dashboard(request):
    return render(request, 'dashboard/dashbordcba.html')

def aboutnorsu_dashboard(request):
    return render(request, 'dashboard/aboutnorsu/aboutnorsu-dashboard.html')

def aboutnorsu(request):
    return render(request, 'dashboard/aboutnorsu.html')
   

def news(request):
    # Get published posts by category for the news page
    # FILTER: Only show Superadmin posts (college='all') in "Latest News"
    general_posts = Post.objects.filter(status='published', category='general', college='all').order_by('-created_at')
    event_posts = Post.objects.filter(status='published', category='event', college='all').order_by('-created_at')
    academic_posts = Post.objects.filter(status='published', category='academic', college='all').order_by('-created_at')
    sports_posts = Post.objects.filter(status='published', category='sports', college='all').order_by('-created_at')
    
    # Get latest achievements for the news page
    achievements = Achievement.objects.filter(status='published').order_by('-created_at')[:6]
    
    # Get college administrator posts for "COLLEGES ANNOUNCEMENT"
    # We want the latest post for each specific college to use as a thumbnail
    colleges = ['cas', 'cted', 'caf', 'ccje', 'cba', 'cit']
    college_latest_posts = {}
    
    for code in colleges:
        latest = Post.objects.filter(status='published', college=code).order_by('-created_at').first()
        if latest:
            college_latest_posts[code] = latest
    
    return render(request, 'dashboard/newsdashbord.html', {
        'general_posts': general_posts,
        'event_posts': event_posts,
        'academic_posts': academic_posts,
        'sports_posts': sports_posts,
        'achievements': achievements,
        'college_latest_posts': college_latest_posts,
    })

def news1(request):
    return render(request, 'dashboard/news/news1.html')

def programs(request):
    return render(request, 'dashboard/news/programs.html')

def alumni(request):
    # Get latest alumni-specific news (fetch up to 10 for the slider)
    latest_news = AlumniNews.objects.filter(status='published').order_by('-created_at')[:10]
    
    # Get upcoming alumni-specific events
    upcoming_events = AlumniEvent.objects.filter(status='published').order_by('-date')[:3]
    
    # Get featured alumni / success stories (using AlumniSuccessStory model)
    featured_achievements = AlumniSuccessStory.objects.filter(status='published').order_by('-created_at')[:3]
    
    # Get Alumni About data safely
    try:
        about_data = AlumniAbout.objects.first()
    except Exception:
        about_data = None
    
    return render(request, 'dashboard/alumni/home.html', {
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
        'featured_achievements': featured_achievements,
        'about_data': about_data
    })

def alumni_about(request):
    try:
        about_data = AlumniAbout.objects.first()
    except Exception:
        about_data = None
        
    return render(request, 'dashboard/alumni/about.html', {
        'about_data': about_data
    })

def alumni_achievements(request):
    achievements = AlumniSuccessStory.objects.filter(status='published').order_by('-created_at')
    search = request.GET.get('search')
    
    if search:
        achievements = achievements.filter(Q(alumni_name__icontains=search) | Q(achievement__icontains=search) | Q(description__icontains=search))
        
    context = {
        'notable_alumni': achievements,
    }
    return render(request, 'dashboard/alumni/achievements.html', context)

def alumni_careers(request):
    return render(request, 'dashboard/alumni/careers.html')

def alumni_contact(request):
    return render(request, 'dashboard/alumni/contact.html')

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def alumni_api(request, pk=None):
    """
    API endpoint for Alumni CRUD operations in the admin dashboard.
    """
    if request.method == 'GET':
        if pk:
            try:
                alumnus = Alumni.objects.get(pk=pk)
                return JsonResponse({
                    'success': True,
                    'alumni': {
                        'id': alumnus.id,
                        'full_name': alumnus.name,
                        'latin_honors': alumnus.latin_honors,
                        'graduation_year': alumnus.batch,
                        'course': alumnus.course,
                        'position': alumnus.position,
                        'company': alumnus.company,
                        'bio': alumnus.bio,
                        'profile_image': alumnus.image.url if alumnus.image else None,
                    }
                })
            except Alumni.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Alumni not found'}, status=404)
        else:
            alumni_list = Alumni.objects.all().order_by('-created_at')
            
            # Filtering
            year = request.GET.get('year')
            course = request.GET.get('course')
            if year:
                alumni_list = alumni_list.filter(batch=year)
            if course:
                alumni_list = alumni_list.filter(course__icontains=course)
                
            data = []
            for a in alumni_list:
                data.append({
                    'id': a.id,
                    'full_name': a.name,
                    'latin_honors': a.latin_honors,
                    'graduation_year': a.batch,
                    'course': a.course,
                    'position': a.position,
                    'company': a.company,
                    'bio': a.bio,
                    'profile_image': a.image.url if a.image else None,
                })
            return JsonResponse({'success': True, 'alumni': data})

    elif request.method == 'POST':
        try:
            # Handle both create and update
            alumni_id = request.POST.get('id')
            name = request.POST.get('name')
            latin_honors = request.POST.get('latin_honors', '')
            batch = request.POST.get('batch')
            course = request.POST.get('course')
            position = request.POST.get('position', '')
            company = request.POST.get('company', '')
            bio = request.POST.get('bio', '')
            image = request.FILES.get('image')

            if alumni_id:
                alumnus = Alumni.objects.get(pk=alumni_id)
                alumnus.name = name
                alumnus.latin_honors = latin_honors
                alumnus.batch = batch
                alumnus.course = course
                alumnus.position = position
                alumnus.company = company
                alumnus.bio = bio
                if image:
                    alumnus.image = image
                alumnus.save()
                message = 'Alumni updated successfully'
            else:
                alumnus = Alumni.objects.create(
                    name=name,
                    latin_honors=latin_honors,
                    batch=batch,
                    course=course,
                    position=position,
                    company=company,
                    bio=bio,
                    image=image
                )
                message = 'Alumni added successfully'

            return JsonResponse({'success': True, 'message': message, 'id': alumnus.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            if not pk:
                return JsonResponse({'success': False, 'error': 'ID required'}, status=400)
            alumnus = Alumni.objects.get(pk=pk)
            alumnus.delete()
            return JsonResponse({'success': True, 'message': 'Alumni deleted successfully'})
        except Alumni.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Alumni not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def alumni_directory(request):
    program = request.GET.get('program')
    year = request.GET.get('year')
    query = request.GET.get('q')
    
    # Get alumni from dedicated Alumni model
    alumni_list = list(Alumni.objects.all())
    
    # Also include alumni entries from the generic Post model
    # (some entries might have been added as 'alumni' type posts)
    alumni_posts = Post.objects.filter(post_type='alumni')
    
    # Map Post objects to a format similar to Alumni model
    for post in alumni_posts:
        alumni_list.append({
            'name': post.title,
            'course': post.content, # Post content often used as course for alumni types
            'batch': 'N/A', # Posts don't have batch
            'latin_honors': '',
            'image': post.image,
            'position': '',
            'company': '',
            'is_post': True
        })
    
    # Now filter the combined list
    filtered_alumni = []
    
    # Filtering logic for combined list
    core_name = ""
    if program:
        p_lower = program.lower()
        core_name = p_lower.replace('bachelor of science in ', '') \
                           .replace('bachelor of ', '') \
                           .replace('bs in ', '') \
                           .replace('bs ', '') \
                           .replace('college of ', '') \
                           .replace('&', 'and') \
                           .strip()
        core_alt = core_name.replace('and', '&')

    for a in alumni_list:
        # Normalize alumni object (handle both dict and model)
        a_name = a['name'] if isinstance(a, dict) else a.name
        a_course = a['course'] if isinstance(a, dict) else a.course
        a_batch = a['batch'] if isinstance(a, dict) else a.batch
        a_position = a['position'] if isinstance(a, dict) else a.position
        a_company = a['company'] if isinstance(a, dict) else a.company
        
        keep = True
        
        if program:
            c_lower = a_course.lower()
            if core_name not in c_lower and program.lower() not in c_lower and core_alt not in c_lower:
                keep = False
                
        if keep and year:
            if str(a_batch) != str(year):
                keep = False
                
        if keep and query:
            q_lower = query.lower()
            if q_lower not in a_name.lower() and \
               q_lower not in a_course.lower() and \
               q_lower not in a_position.lower() and \
               q_lower not in a_company.lower():
                keep = False
                
        if keep:
            filtered_alumni.append(a)
        
    return render(request, 'dashboard/alumni/directory.html', {
        'alumni': filtered_alumni,
        'selected_program': program,
        'selected_year': year,
        'query': query
    })

def alumni_events(request):
    events = AlumniEvent.objects.filter(status='published').order_by('-date')
    return render(request, 'dashboard/alumni/events.html', {'events': events})

def alumni_gallery(request):
    return render(request, 'dashboard/alumni/gallery.html')

def alumni_programs(request):
    return render(request, 'dashboard/alumni/programs.html')

def alumni_news(request):
    news_id = request.GET.get('id')
    if news_id:
        try:
            # Show only the specific article requested
            news_items = AlumniNews.objects.filter(id=news_id, status='published')
        except (AlumniNews.DoesNotExist, ValueError):
            news_items = AlumniNews.objects.filter(status='published').order_by('-created_at')
    else:
        # Show all news articles
        news_items = AlumniNews.objects.filter(status='published').order_by('-created_at')
        
    return render(request, 'dashboard/alumni/news.html', {'news': news_items, 'single_view': bool(news_id)})

def alumni_upload_media(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            media_type = request.POST.get('media_type')
            year = request.POST.get('year')
            college = request.POST.get('college')
            file = request.FILES.get('file')
            
            if not all([title, media_type, year, college, file]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'dashboard/alumni/upload_media.html')
            
            # Create media upload with pending status
            media_upload = MediaUpload.objects.create(
                title=title,
                description=description,
                media_type=media_type,
                file=file,
                year=year,
                college=college,
                uploaded_by=request.user.username if request.user.is_authenticated else 'Anonymous Alumni',
                approval_status='pending'
            )
            
            messages.success(request, 'Your media has been uploaded successfully! It will be reviewed by the admin before being published.')
            return redirect('gallery')
            
        except Exception as e:
            messages.error(request, f'Error uploading media: {str(e)}')
            return render(request, 'dashboard/alumni/upload_media.html')
    
    return render(request, 'dashboard/alumni/upload_media.html')

def alumni_dashboard(request):
    return render(request, 'dashboard/alumnidasbord.html')


# Media Upload Management API Endpoints

def get_media_uploads(request):
    """Get all media uploads for admin approval"""
    uploads = MediaUpload.objects.all().order_by('-created_at')
    uploads_data = []
    for upload in uploads:
        uploads_data.append({
            'id': upload.id,
            'title': upload.title,
            'description': upload.description,
            'media_type': upload.media_type,
            'file_url': upload.file.url if upload.file else '',
            'file_name': upload.file.name.split('/')[-1] if upload.file else '',
            'year': upload.year,
            'college': upload.college,
            'uploaded_by': upload.uploaded_by,
            'approval_status': upload.approval_status,
            'rejection_reason': upload.rejection_reason,
            'created_at': upload.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({'uploads': uploads_data})

@csrf_exempt
def approve_media_upload(request, upload_id):
    """Approve a media upload"""
    if request.method == 'POST':
        try:
            upload = MediaUpload.objects.get(id=upload_id)
            upload.approval_status = 'approved'
            upload.save()
            return JsonResponse({'success': True, 'message': 'Media upload approved successfully'})
        except MediaUpload.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Media upload not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def reject_media_upload(request, upload_id):
    """Reject a media upload"""
    if request.method == 'POST':
        try:
            upload = MediaUpload.objects.get(id=upload_id)
            upload.approval_status = 'rejected'
            rejection_reason = request.POST.get('rejection_reason', '')
            upload.rejection_reason = rejection_reason
            upload.save()
            return JsonResponse({'success': True, 'message': 'Media upload rejected successfully'})
        except MediaUpload.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Media upload not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def delete_media_upload(request, upload_id):
    """Delete a media upload"""
    if request.method == 'POST':
        try:
            upload = MediaUpload.objects.get(id=upload_id)
            # Delete the file
            if upload.file:
                upload.file.delete()
            upload.delete()
            return JsonResponse({'success': True, 'message': 'Media upload deleted successfully'})
        except MediaUpload.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Media upload not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# Post Management API Endpoints

def get_posts(request):
    """
    API endpoint to retrieve all posts.
    Returns JSON response with success flag and posts array.
    """
    college = request.GET.get('college')
    post_type = request.GET.get('type')
    
    posts = Post.objects.all()
    
    if college and college != 'all':
        posts = posts.filter(college__iexact=college)
    if post_type:
        posts = posts.filter(post_type=post_type)
        
    posts_data = []
    for post in posts:
        post_dict = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'post_type': post.post_type,
            'category': post.category,
            'college': post.college,
            'target_audience': post.target_audience,
            'image': post.image.url if post.image else '',
            'status': post.status,
            'author': post.author,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            # Support legacy field names if any
            'date': post.created_at.isoformat(),
            'type': post.post_type,
        }
        posts_data.append(post_dict)
    
    return JsonResponse({
        'success': True,
        'posts': posts_data
    })


@csrf_exempt
def create_post(request):
    """
    API endpoint to create a new post.
    Accepts POST requests with post data and returns success JSON.
    """
    if request.method == 'POST':
        try:
            # Extract data from POST request
            post_id = request.POST.get('id')
            title = request.POST.get('title')
            content = request.POST.get('content')
            post_type = request.POST.get('type', 'general')
            category = request.POST.get('category', 'general')
            college = request.POST.get('college', 'all').lower()
            target_audience = request.POST.get('target_audience', 'all')
            status = request.POST.get('status', 'published')
            author = request.POST.get('author')
            
            # Handle image upload if present
            image = request.FILES.get('image', None)
            
            if post_id:
                # Update existing
                post = Post.objects.get(id=post_id)
                post.title = title
                post.content = content
                post.post_type = post_type
                post.category = category
                post.college = college
                post.target_audience = target_audience
                post.status = status
                if author:
                    post.author = author
                if image:
                    post.image = image
                post.save()
                message = 'Post updated successfully'
            else:
                # Create new Post instance
                post = Post.objects.create(
                    title=title,
                    content=content,
                    post_type=post_type,
                    category=category,
                    college=college,
                    target_audience=target_audience,
                    status=status,
                    author=author,
                    image=image
                )
                message = 'Post created successfully'
            
            # Return success response with created post data
            return JsonResponse({
                'success': True,
                'message': message,
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'post_type': post.post_type,
                    'image': post.image.url if post.image else '',
                    'created_at': post.created_at.isoformat(),
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


# Academic Calendar Views

def academic_calendar(request):
    """
    Public view for the Academic Calendar.
    Displays images and description for the active academic calendar.
    """
    # Get the latest active academic calendar
    calendar = AcademicCalendar.objects.filter(is_active=True).order_by('-created_at').first()
    
    context = {
        'calendar': calendar,
    }
    
    return render(request, 'dashboard/academic_calendar.html', context)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_calendar_list_create(request):
    """
    API endpoint to list (GET) or create (POST) calendar entries.
    """
    if request.method == 'GET':
        calendars = AcademicCalendar.objects.all().order_by('-created_at')
        
        data = []
        for cal in calendars:
            data.append({
                'id': cal.id,
                'title': cal.title,
                'academic_year': cal.academic_year,
                'description': cal.description,
                'images': cal.images or [],
                'pdf_url': cal.pdf_file.url if cal.pdf_file else None,
                'is_active': cal.is_active,
                'created_at': cal.created_at.isoformat(),
            })
            
        return JsonResponse({
            'success': True,
            'calendars': data
        })
        
    elif request.method == 'POST':
        try:
            title = request.POST.get('title', 'Academic Calendar')
            academic_year = request.POST.get('academic_year', '2025-2026')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == 'true'
            
            # Handle PDF upload
            pdf_file = request.FILES.get('pdf_file')
            
            # Handle multiple image uploads
            calendar_images = []
            files = request.FILES.getlist('images')
            if files:
                import os
                from django.core.files.storage import default_storage
                for f in files:
                    # Save to media/calendar/
                    path = default_storage.save(f'calendar/{f.name}', f)
                    calendar_images.append(default_storage.url(path))
            
            # If this is active, deactivate others
            if is_active:
                AcademicCalendar.objects.filter(is_active=True).update(is_active=False)
            
            calendar = AcademicCalendar.objects.create(
                title=title,
                academic_year=academic_year,
                description=description,
                images=calendar_images,
                pdf_file=pdf_file,
                is_active=is_active
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Calendar created successfully',
                'calendar': {
                    'id': calendar.id,
                    'title': calendar.title,
                    'academic_year': calendar.academic_year,
                    'images': calendar.images,
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_calendar_detail(request, pk):
    """
    API endpoint to update (POST/PUT) or delete (DELETE) a calendar entry.
    """
    try:
        calendar = AcademicCalendar.objects.get(pk=pk)
    except AcademicCalendar.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Calendar not found'}, status=404)
        
    if request.method in ['POST', 'PUT']:
        try:
            calendar.title = request.POST.get('title', calendar.title)
            calendar.academic_year = request.POST.get('academic_year', calendar.academic_year)
            calendar.description = request.POST.get('description', calendar.description)
            
            is_active_val = request.POST.get('is_active')
            if is_active_val is not None:
                new_is_active = is_active_val == 'true'
                if new_is_active and not calendar.is_active:
                    # Deactivate others if this one is becoming active
                    AcademicCalendar.objects.filter(is_active=True).update(is_active=False)
                calendar.is_active = new_is_active
            
            # Handle new images
            files = request.FILES.getlist('images')
            if files:
                import os
                from django.core.files.storage import default_storage
                new_images = calendar.images or []
                for f in files:
                    path = default_storage.save(f'calendar/{f.name}', f)
                    new_images.append(default_storage.url(path))
                calendar.images = new_images
            
            # Handle new PDF
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                calendar.pdf_file = pdf_file
            
            calendar.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Calendar updated successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        try:
            calendar.delete()
            return JsonResponse({
                'success': True,
                'message': 'Calendar deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


# Achievement Management API Endpoints

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def achievement_list_create(request):
    """
    API endpoint to list all achievements (GET) or create/update an achievement (POST).
    """
    if request.method == 'GET':
        achievements = Achievement.objects.all().order_by('-created_at')
        achievements_data = []
        for achievement in achievements:
            achievements_data.append({
                'id': achievement.id,
                'title': achievement.title,
                'description': achievement.description,
                'category': achievement.category,
                'recipient': achievement.recipient,
                'achievement_date': achievement.achievement_date.isoformat() if achievement.achievement_date else '',
                'image': achievement.image.url if achievement.image else '',
                'status': achievement.status,
            })
        return JsonResponse({'success': True, 'achievements': achievements_data})
    
    elif request.method == 'POST':
        try:
            achievement_id = request.POST.get('id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            category = request.POST.get('category', 'other')
            recipient = request.POST.get('recipient')
            achievement_date = request.POST.get('achievement_date')
            status = request.POST.get('status', 'published')
            image = request.FILES.get('image')

            if achievement_id:
                achievement = Achievement.objects.get(id=achievement_id)
                achievement.title = title
                achievement.description = description
                achievement.category = category
                achievement.recipient = recipient
                if achievement_date:
                    achievement.achievement_date = achievement_date
                achievement.status = status
                if image:
                    achievement.image = image
                achievement.save()
            else:
                achievement = Achievement.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    recipient=recipient,
                    achievement_date=achievement_date if achievement_date else None,
                    status=status,
                    image=image
                )
            
            return JsonResponse({
                'success': True, 
                'message': 'Achievement saved successfully',
                'achievement': {
                    'id': achievement.id,
                    'title': achievement.title,
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
@login_required(login_url='/super-admin-login/')
def success_story_list_create(request):
    """
    API endpoint to list all alumni success stories (GET) or create/update a success story (POST).
    """
    if request.method == 'GET':
        stories = AlumniSuccessStory.objects.all().order_by('-created_at')
        stories_data = []
        for story in stories:
            stories_data.append({
                'id': story.id,
                'alumni_name': story.alumni_name,
                'achievement': story.achievement,
                'description': story.description,
                'image': story.image.url if story.image else '',
                'status': story.status,
            })
        return JsonResponse({'success': True, 'stories': stories_data})
    
    elif request.method == 'POST':
        try:
            story_id = request.POST.get('id')
            alumni_name = request.POST.get('alumni_name')
            achievement = request.POST.get('achievement')
            description = request.POST.get('description')
            status = request.POST.get('status', 'published')
            image = request.FILES.get('image')

            if story_id:
                story = AlumniSuccessStory.objects.get(id=story_id)
                story.alumni_name = alumni_name
                story.achievement = achievement
                story.description = description
                story.status = status
                if image:
                    story.image = image
                story.save()
            else:
                story = AlumniSuccessStory.objects.create(
                    alumni_name=alumni_name,
                    achievement=achievement,
                    description=description,
                    status=status,
                    image=image
                )
            
            return JsonResponse({
                'success': True, 
                'message': 'Success story saved successfully',
                'story': {
                    'id': story.id,
                    'alumni_name': story.alumni_name,
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def success_story_detail(request, pk):
    """
    API endpoint to get or delete a success story.
    """
    try:
        story = AlumniSuccessStory.objects.get(pk=pk)
    except AlumniSuccessStory.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Success story not found'}, status=404)
        
    if request.method == 'GET':
        return JsonResponse({
            'success': True,
            'story': {
                'id': story.id,
                'alumni_name': story.alumni_name,
                'achievement': story.achievement,
                'description': story.description,
                'image': story.image.url if story.image else '',
                'status': story.status,
            }
        })
    elif request.method == 'DELETE' or request.method == 'POST':
        try:
            story.delete()
            return JsonResponse({'success': True, 'message': 'Success story deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def achievement_detail(request, pk):
    """
    API endpoint to get or delete an achievement.
    """
    try:
        achievement = Achievement.objects.get(pk=pk)
    except Achievement.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Achievement not found'}, status=404)
        
    if request.method == 'GET':
        return JsonResponse({
            'success': True,
            'achievement': {
                'id': achievement.id,
                'title': achievement.title,
                'description': achievement.description,
                'category': achievement.category,
                'recipient': achievement.recipient,
                'achievement_date': achievement.achievement_date.isoformat() if achievement.achievement_date else '',
                'image': achievement.image.url if achievement.image else '',
                'status': achievement.status,
            }
        })
    elif request.method == 'DELETE' or request.method == 'POST':
        try:
            achievement.delete()
            return JsonResponse({'success': True, 'message': 'Achievement deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)


# College Management API Endpoints

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def college_list_create(request):
    """
    API endpoint to list all colleges (GET) or create/update a college (POST).
    """
    if request.method == 'GET':
        colleges = College.objects.all().order_by('name')
        colleges_data = []
        for college in colleges:
            colleges_data.append({
                'id': college.id,
                'name': college.name,
                'abbreviation': college.abbreviation,
                'dean': college.dean,
                'students': college.total_students,
                'programs': college.programs_offered,
                'instructors': college.qualified_instructors,
                'status': college.status,
                'description': college.description,
                'image': college.image.url if college.image else '',
            })
        return JsonResponse({'success': True, 'colleges': colleges_data})
    
    elif request.method == 'POST':
        try:
            college_id = request.POST.get('id')
            name = request.POST.get('name')
            abbreviation = request.POST.get('abbreviation')
            dean = request.POST.get('dean')
            students = request.POST.get('students', 0)
            programs = request.POST.get('programs', 0)
            instructors = request.POST.get('instructors', 0)
            status = request.POST.get('status', 'active')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            if college_id:
                college = College.objects.get(id=college_id)
                college.name = name
                college.abbreviation = abbreviation
                college.dean = dean
                college.total_students = _safe_int(students)
                college.programs_offered = _safe_int(programs)
                college.qualified_instructors = _safe_int(instructors)
                college.status = status
                college.description = description
                if image:
                    college.image = image
                college.save()
            else:
                college = College.objects.create(
                    name=name,
                    abbreviation=abbreviation,
                    dean=dean,
                    total_students=_safe_int(students),
                    programs_offered=_safe_int(programs),
                    qualified_instructors=_safe_int(instructors),
                    status=status,
                    description=description,
                    image=image
                )
            
            return JsonResponse({
                'success': True, 
                'message': 'College saved successfully',
                'college': {
                    'id': college.id,
                    'name': college.name,
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def college_detail(request, pk):
    """
    API endpoint to get or delete a college.
    """
    try:
        college = College.objects.get(pk=pk)
    except College.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'College not found'}, status=404)
        
    if request.method == 'GET':
        return JsonResponse({
            'success': True,
            'college': {
                'id': college.id,
                'name': college.name,
                'abbreviation': college.abbreviation,
                'dean': college.dean,
                'students': college.total_students,
                'programs': college.programs_offered,
                'instructors': college.qualified_instructors,
                'status': college.status,
                'description': college.description,
                'image': college.image.url if college.image else '',
            }
        })
    elif request.method == 'DELETE' or request.method == 'POST':
        try:
            college.delete()
            return JsonResponse({'success': True, 'message': 'College deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)





@csrf_exempt
def delete_post(request, post_id):
    """
    API endpoint to delete a post.
    Accepts DELETE requests and returns success JSON.
    """
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({
                'success': True,
                'message': 'Post deleted successfully'
            })
        except Post.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Post not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_alumni_news(request):
    if request.method == 'GET':
        news = AlumniNews.objects.all().order_by('-created_at')
        news_data = []
        for n in news:
            news_data.append({
                'id': n.id,
                'title': n.title,
                'content': n.content,
                'image': n.image.url if n.image else '',
                'created_at': n.created_at.isoformat(),
                'status': n.status
            })
        return JsonResponse({'success': True, 'news': news_data})
    
    elif request.method == 'POST':
        try:
            news_id = request.POST.get('id')
            if news_id:
                news_item = AlumniNews.objects.get(id=news_id)
            else:
                news_item = AlumniNews()
            
            news_item.title = request.POST.get('title')
            news_item.content = request.POST.get('content')
            news_item.status = request.POST.get('status', 'published')
            
            if request.FILES.get('image'):
                news_item.image = request.FILES.get('image')
            
            news_item.save()
            return JsonResponse({'success': True, 'message': 'Alumni news saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_alumni_events(request):
    if request.method == 'GET':
        events = AlumniEvent.objects.all().order_by('-date')
        events_data = []
        for e in events:
            events_data.append({
                'id': e.id,
                'title': e.title,
                'description': e.description,
                'date': e.date.isoformat(),
                'location': e.location,
                'image': e.image.url if e.image else '',
                'status': e.status
            })
        return JsonResponse({'success': True, 'events': events_data})
    
    elif request.method == 'POST':
        try:
            event_id = request.POST.get('id')
            if event_id:
                event = AlumniEvent.objects.get(id=event_id)
            else:
                event = AlumniEvent()
            
            event.title = request.POST.get('title')
            event.description = request.POST.get('description')
            event.date = request.POST.get('date')
            event.location = request.POST.get('location')
            event.status = request.POST.get('status', 'published')
            
            if request.FILES.get('image'):
                event.image = request.FILES.get('image')
            
            event.save()
            return JsonResponse({'success': True, 'message': 'Alumni event saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_alumni_news_delete(request, pk):
    if request.method == 'POST':
        try:
            item = AlumniNews.objects.get(id=pk)
            item.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_alumni_events_delete(request, pk):
    if request.method == 'POST':
        try:
            item = AlumniEvent.objects.get(id=pk)
            item.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@login_required(login_url='/super-admin-login/')
def api_alumni_about(request):
    """
    API endpoint to get (GET) or update (POST) the Alumni About information.
    """
    if request.method == 'GET':
        about = AlumniAbout.objects.first()
        if not about:
            # Create a default one if none exists
            about = AlumniAbout.objects.create(
                title='The NORSU-BSC Alumni Association',
                content="We are a vibrant community of graduates dedicated to fostering lifelong relationships between Negros Oriental State University and its alumni. Through networking, mentorship, and support, we empower our members to achieve excellence in their respective fields.",
                vision="A globally recognized state university.",
                mission="To build a strong, supportive network that champions the success of NORSUnians and contributes to the institution's enduring legacy of academic excellence."
            )
        
        return JsonResponse({
            'success': True,
            'about': {
                'id': about.id,
                'title': about.title,
                'content': about.content,
                'vision': about.vision,
                'mission': about.mission,
                'image': about.image.url if about.image else ''
            }
        })
    
    elif request.method == 'POST':
        try:
            about = AlumniAbout.objects.first()
            if not about:
                about = AlumniAbout()
            
            about.title = request.POST.get('title', about.title)
            about.content = request.POST.get('content', about.content)
            about.vision = request.POST.get('vision', about.vision)
            about.mission = request.POST.get('mission', about.mission)
            
            image = request.FILES.get('image')
            if image:
                about.image = image
            
            about.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Alumni About information updated successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


# Faculty Management API Endpoints

@csrf_exempt
def faculty_list_create(request):
    """
    API endpoint to list all faculty members (GET) or create a new faculty member (POST).
    """
    if request.method == 'GET':
        college = request.GET.get('college')
        if college:
            faculty = Faculty.objects.filter(college__iexact=college)
        else:
            faculty = Faculty.objects.all()
            
        faculty_data = []
        for member in faculty:
            faculty_data.append({
                'id': member.id,
                'name': member.name,
                'position': member.position,
                'college': member.college,
                'status': member.status,
                'image': member.image.url if member.image else '',
                'created_at': member.created_at.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'faculty': faculty_data
        })
    
    elif request.method == 'POST':
        try:
            name = request.POST.get('name')
            position = request.POST.get('position')
            college = request.POST.get('college').lower() if request.POST.get('college') else None
            status = request.POST.get('status', 'active')
            image = request.FILES.get('image')
            
            faculty_id = request.POST.get('id')
            if faculty_id:
                # Update existing
                member = Faculty.objects.get(id=faculty_id)
                member.name = name
                member.position = position
                member.college = college
                member.status = status
                if image:
                    member.image = image
                member.save()
            else:
                # Create new
                member = Faculty.objects.create(
                    name=name,
                    position=position,
                    college=college,
                    status=status,
                    image=image
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Faculty member saved successfully',
                'faculty': {
                    'id': member.id,
                    'name': member.name,
                    'position': member.position,
                    'college': member.college,
                    'status': member.status,
                    'image': member.image.url if member.image else '',
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def faculty_delete(request, pk):
    """
    API endpoint to delete a faculty member.
    """
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            member = Faculty.objects.get(pk=pk)
            member.delete()
            return JsonResponse({'success': True, 'message': 'Faculty member deleted successfully'})
        except Faculty.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Faculty member not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)


# Facility Management API Endpoints

@csrf_exempt
def facility_list_create(request):
    """
    API endpoint to list all facilities (GET) or create a new facility (POST).
    """
    if request.method == 'GET':
        college = request.GET.get('college')
        if college:
            facilities = Facility.objects.filter(college__iexact=college)
        else:
            facilities = Facility.objects.all()
            
        facilities_data = []
        for facility in facilities:
            facilities_data.append({
                'id': facility.id,
                'name': facility.name,
                'type': facility.type,
                'capacity': facility.capacity,
                'college': facility.college,
                'status': facility.status,
                'image': facility.image.url if facility.image else '',
            })
        
        return JsonResponse({
            'success': True,
            'facilities': facilities_data
        })
    
    elif request.method == 'POST':
        try:
            name = request.POST.get('name')
            facility_type = request.POST.get('type')
            capacity = request.POST.get('capacity')
            college = request.POST.get('college').lower() if request.POST.get('college') else None
            status = request.POST.get('status', 'available')
            image = request.FILES.get('image')
            
            facility_id = request.POST.get('id')
            if facility_id:
                # Update
                facility = Facility.objects.get(id=facility_id)
                facility.name = name
                facility.type = facility_type
                facility.capacity = capacity
                facility.college = college
                facility.status = status
                if image:
                    facility.image = image
                facility.save()
            else:
                # Create
                facility = Facility.objects.create(
                    name=name,
                    type=facility_type,
                    capacity=capacity,
                    college=college,
                    status=status,
                    image=image
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Facility saved successfully',
                'facility': {
                    'id': facility.id,
                    'name': facility.name,
                    'image': facility.image.url if facility.image else '',
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def facility_delete(request, pk):
    """
    API endpoint to delete a facility.
    """
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            facility = Facility.objects.get(pk=pk)
            facility.delete()
            return JsonResponse({'success': True, 'message': 'Facility deleted successfully'})
        except Facility.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Facility not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)


@csrf_exempt
def delete_post(request, post_id):
    """
    API endpoint to delete a post by ID.
    Accepts POST requests with post ID and returns success JSON.
    """
    if request.method == 'POST':
        try:
            # Retrieve and delete the post
            post = Post.objects.get(id=post_id)
            post.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Post deleted successfully'
            })
        except Post.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Post not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


# Program Management API Endpoints

@csrf_exempt
def program_list_create(request):
    """
    API endpoint to list all programs (GET) or create a new program (POST).
    GET: Returns JSON response with all programs.
    POST: Creates a new program and returns the created program data.
    """
    if request.method == 'GET':
        college = request.GET.get('college')
        if college:
            programs = Program.objects.filter(college__iexact=college)
        else:
            programs = Program.objects.all()
        programs_data = []
        
        for program in programs:
            program_dict = {
                'id': program.id,
                'title': program.title,
                'description': program.description,
                'level': program.level,
                'college': program.college,
                'duration': program.duration,
                'objectives': program.objectives,
                'dresscode_schedule': program.dresscode_schedule,
                'dresscode_images': program.dresscode_images or [],
                'vision': program.vision,
                'mission': program.mission,
                'image': program.image.url if program.image else '',
                'status': program.status,
                'created_at': program.created_at.isoformat(),
                'updated_at': program.updated_at.isoformat(),
            }
            programs_data.append(program_dict)
        
        return JsonResponse({
            'success': True,
            'programs': programs_data
        })
    
    elif request.method == 'POST':
        try:
            # Extract data from POST request
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            level = request.POST.get('level', 'undergraduate')
            college = request.POST.get('college').lower() if request.POST.get('college') else None
            duration = request.POST.get('duration', '')
            objectives = request.POST.get('objectives', '')
            dresscode_schedule = request.POST.get('dresscode_schedule', '')
            vision = request.POST.get('vision', '')
            mission = request.POST.get('mission', '')
            status = request.POST.get('status', 'published')
            
            # Validate required fields
            if not title:
                return JsonResponse({
                    'success': False,
                    'error': 'Title is required'
                }, status=400)
            
            if not college:
                return JsonResponse({
                    'success': False,
                    'error': 'College is required'
                }, status=400)
            
            # Handle image upload if present
            image = request.FILES.get('image', None)
            
            # Handle multiple dresscode images
            import json as _json
            dresscode_images = []
            for f in request.FILES.getlist('dresscode_images'):
                import os
                from django.core.files.storage import default_storage
                path = default_storage.save(f'programs/dresscode/{f.name}', f)
                dresscode_images.append(default_storage.url(path))
            
            # Create new Program instance
            program = Program.objects.create(
                title=title,
                description=description,
                level=level,
                college=college,
                duration=duration,
                objectives=objectives,
                dresscode_schedule=dresscode_schedule,
                dresscode_images=dresscode_images,
                vision=vision,
                mission=mission,
                status=status,
                image=image
            )
            
            # Return success response with created program data
            return JsonResponse({
                'success': True,
                'message': 'Program created successfully',
                'program': {
                    'id': program.id,
                    'title': program.title,
                    'description': program.description,
                    'level': program.level,
                    'college': program.college,
                    'duration': program.duration,
                    'objectives': program.objectives,
                    'dresscode_schedule': program.dresscode_schedule,
                    'dresscode_images': program.dresscode_images or [],
                    'vision': program.vision,
                    'mission': program.mission,
                    'image': program.image.url if program.image else '',
                    'status': program.status,
                    'created_at': program.created_at.isoformat(),
                    'updated_at': program.updated_at.isoformat(),
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


@csrf_exempt
def program_detail(request, pk):
    """
    API endpoint to retrieve (GET), update (PUT), or delete (DELETE) a specific program.
    GET: Returns the program data.
    PUT: Updates the program and returns updated data.
    DELETE: Deletes the program and returns success message.
    """
    try:
        program = Program.objects.get(pk=pk)
    except Program.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Program not found'
        }, status=404)
    
    if request.method == 'GET':
        # Retrieve program details
        program_dict = {
            'id': program.id,
            'title': program.title,
            'description': program.description,
            'level': program.level,
            'college': program.college,
            'duration': program.duration,
            'objectives': program.objectives,
            'dresscode_schedule': program.dresscode_schedule,
            'dresscode_images': program.dresscode_images or [],
            'vision': program.vision,
            'mission': program.mission,
            'image': program.image.url if program.image else '',
            'status': program.status,
            'created_at': program.created_at.isoformat(),
            'updated_at': program.updated_at.isoformat(),
        }
        
        return JsonResponse({
            'success': True,
            'program': program_dict
        })
    
    elif request.method == 'PUT' or request.method == 'POST':
        # Handle both PUT and POST for update (some clients use POST for updates)
        try:
            # Extract data from request
            title = request.POST.get('title')
            description = request.POST.get('description')
            level = request.POST.get('level')
            college = request.POST.get('college')
            duration = request.POST.get('duration')
            objectives = request.POST.get('objectives')
            dresscode_schedule = request.POST.get('dresscode_schedule')
            vision = request.POST.get('vision')
            mission = request.POST.get('mission')
            status = request.POST.get('status')
            
            # Update fields if provided
            if title:
                program.title = title
            if description is not None:
                program.description = description
            if level:
                program.level = level
            if college:
                program.college = college
            if duration is not None:
                program.duration = duration
            if objectives is not None:
                program.objectives = objectives
            if dresscode_schedule is not None:
                program.dresscode_schedule = dresscode_schedule
            if vision is not None:
                program.vision = vision
            if mission is not None:
                program.mission = mission
            if status:
                program.status = status
            
            # Handle image upload if present
            if 'image' in request.FILES:
                program.image = request.FILES['image']
            
            # Handle dresscode images (append new ones)
            new_dresscode_files = request.FILES.getlist('dresscode_images')
            if new_dresscode_files:
                from django.core.files.storage import default_storage
                existing = program.dresscode_images or []
                for f in new_dresscode_files:
                    path = default_storage.save(f'programs/dresscode/{f.name}', f)
                    existing.append(default_storage.url(path))
                program.dresscode_images = existing
            
            program.save()
            
            # Return success response with updated program data
            return JsonResponse({
                'success': True,
                'message': 'Program updated successfully',
                'program': {
                    'id': program.id,
                    'title': program.title,
                    'description': program.description,
                    'level': program.level,
                    'college': program.college,
                    'duration': program.duration,
                    'objectives': program.objectives,
                    'dresscode_schedule': program.dresscode_schedule,
                    'dresscode_images': program.dresscode_images or [],
                    'vision': program.vision,
                    'mission': program.mission,
                    'image': program.image.url if program.image else '',
                    'status': program.status,
                    'created_at': program.created_at.isoformat(),
                    'updated_at': program.updated_at.isoformat(),
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == 'DELETE':
        try:
            program.delete()
            return JsonResponse({
                'success': True,
                'message': 'Program deleted successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)
