# CAS Dashboard Post Visibility Troubleshooting

## Issue: Post created successfully but not visible in CAS dashboard

## Quick Debugging Steps

### 1. Check Browser Console
Open CAS dashboard (http://127.0.0.1:8000/cas/) and press F12 to open developer tools. Look for any JavaScript errors in the Console tab.

### 2. Check localStorage Data
In browser console, run this command to check what posts exist:
```javascript
console.log('All posts:', JSON.parse(localStorage.getItem('allPosts') || '[]'));
```

### 3. Check Post College Assignment
Look at the posts and verify if any have `college: "cas"`:
```javascript
const allPosts = JSON.parse(localStorage.getItem('allPosts') || '[]');
const casPosts = allPosts.filter(post => post.college === 'cas');
console.log('CAS posts:', casPosts);
```

## Common Issues

### Issue 1: Wrong College Assignment
- **Problem**: Post was created with wrong college (not "cas")
- **Solution**: Ensure you select "CAS" as the college when creating posts

### Issue 2: Data Storage Problem
- **Problem**: Post saved but not stored in localStorage correctly
- **Solution**: Check if posts are being saved to `allPosts` key

### Issue 3: JavaScript Error
- **Problem**: JavaScript error preventing posts from loading
- **Solution**: Check browser console for red error messages

## Manual Test

If you want to quickly test, run this in browser console on CAS dashboard:
```javascript
// Add a test CAS post
const testPost = {
    id: Date.now(),
    title: "Test CAS Post",
    content: "This is a test post to verify CAS dashboard connection.",
    type: "news",
    college: "cas",
    date: new Date().toISOString(),
    image: null
};

const existingPosts = JSON.parse(localStorage.getItem('allPosts') || '[]');
const allPosts = [testPost, ...existingPosts];
localStorage.setItem('allPosts', JSON.stringify(allPosts));

// Refresh to see the post
location.reload();
```

## Expected Results

After creating a CAS post correctly, you should see:
- Post appear in "LATEST AT CAS" section
- Post title, content preview
- Post type badge
- Date formatting
- Professional card layout

## Next Steps

1. Check console for errors
2. Verify localStorage contains posts with `college: "cas"`
3. Try the manual test above
4. If still not working, check the admin dashboard post creation process
