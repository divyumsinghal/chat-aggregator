// Sample data generators
const chatNames = ['Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown', 'Emma Davis', 'Frank Miller', 'Grace Wilson', 'Henry Moore'];

const chatMessages = [
    "Hey everyone, just wanted to check in on the project status.",
    "The meeting has been moved to 3 PM tomorrow.",
    "Can someone review my latest changes?",
    "Great work on the presentation!",
    "I'll be out of office next week.",
    "The new feature is ready for testing.",
    "Thanks for the quick response!",
    "Let's schedule a follow-up meeting.",
    "I've updated the documentation.",
    "The bug has been fixed.",
    "Can we discuss this in more detail?",
    "I agree with that approach.",
    "The deadline has been extended.",
    "Please review the attached file.",
    "I'll send the report by end of day.",
    "The server is back online.",
    "Great job on the release!",
    "I need help with this issue.",
    "The client loved the proposal.",
    "Let's celebrate this milestone!"
];


// Generate random date within last 7 days
function getRandomDate() {
    const now = new Date();
    const daysAgo = Math.floor(Math.random() * 7);
    const hoursAgo = Math.floor(Math.random() * 24);
    const minutesAgo = Math.floor(Math.random() * 60);
    const date = new Date(now);
    date.setDate(date.getDate() - daysAgo);
    date.setHours(date.getHours() - hoursAgo);
    date.setMinutes(date.getMinutes() - minutesAgo);
    return date;
}

function formatDate(date) {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) {
        return `${minutes}m ago`;
    } else if (hours < 24) {
        return `${hours}h ago`;
    } else if (days < 7) {
        return `${days}d ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// Generate fake chat messages for each platform
// Internally generates WhatsApp, Instagram, TikTok, Snapchat but displays as Slack
function generateChatMessages() {
    const allMessages = [];
    // Internal platforms that will be grouped into Slack
    const slackPlatforms = ['WhatsApp', 'Instagram', 'TikTok', 'Snapchat'];
    const otherPlatforms = ['Teams', 'Email'];
    
    // Generate messages per platform
    const messagesPerPlatform = {
        'WhatsApp': 20,
        'Instagram': 30,
        'TikTok': 30,
        'Snapchat': 30,
        'Teams': 30,
        'Email': 30
    };
    
    // Generate Slack messages (from WhatsApp, Instagram, TikTok, Snapchat)
    slackPlatforms.forEach((platform) => {
        const count = messagesPerPlatform[platform] || 3;
        for (let i = 0; i < count; i++) {
            const sender = chatNames[Math.floor(Math.random() * chatNames.length)];
            const content = chatMessages[Math.floor(Math.random() * chatMessages.length)];
            const timestamp = getRandomDate();
            
            allMessages.push({
                id: allMessages.length + 1,
                platform: platform, // Keep original platform for JSON export
                displayPlatform: 'Slack', // For UI display
                sender: sender,
                content: content,
                timestamp: timestamp.toISOString(),
                unread: true
            });
        }
    });
    
    // Generate other platforms
    otherPlatforms.forEach((platform) => {
        const count = messagesPerPlatform[platform] || 3;
        for (let i = 0; i < count; i++) {
            const sender = chatNames[Math.floor(Math.random() * chatNames.length)];
            const content = chatMessages[Math.floor(Math.random() * chatMessages.length)];
            const timestamp = getRandomDate();
            
            allMessages.push({
                id: allMessages.length + 1,
                platform: platform,
                displayPlatform: platform,
                sender: sender,
                content: content,
                timestamp: timestamp.toISOString(),
                unread: true
            });
        }
    });
    
    // Sort by timestamp (newest first)
    return allMessages.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}


// Display chat messages grouped by platform
function displayChatMessages(messages) {
    const platforms = {
        'Email': { container: document.getElementById('email-messages'), badge: document.getElementById('email-badge') },
        'Slack': { container: document.getElementById('slack-messages'), badge: document.getElementById('slack-badge') },
        'Teams': { container: document.getElementById('teams-messages'), badge: document.getElementById('teams-badge') }
    };
    
    // Clear all platform containers
    Object.values(platforms).forEach(platform => {
        if (platform.container) {
            platform.container.innerHTML = '';
        }
    });
    
    // Group messages by display platform
    const messagesByPlatform = {
        'Email': [],
        'Slack': [],
        'Teams': []
    };
    
    messages.forEach(msg => {
        const displayPlatform = msg.displayPlatform || msg.platform;
        // Map WhatsApp, Instagram, TikTok, Snapchat to Slack for display
        if (['WhatsApp', 'Instagram', 'TikTok', 'Snapchat'].includes(msg.platform)) {
            messagesByPlatform['Slack'].push(msg);
        } else if (messagesByPlatform[displayPlatform]) {
            messagesByPlatform[displayPlatform].push(msg);
        }
    });
    
    // Display messages for each platform
    Object.keys(platforms).forEach(platformName => {
        const platformMessages = messagesByPlatform[platformName];
        const platform = platforms[platformName];
        
        if (!platform.container || !platform.badge) return;
        
        // Update badge
        const unreadCount = platformMessages.filter(m => m.unread).length;
        platform.badge.textContent = unreadCount;
        
        // Display messages
        if (platformMessages.length === 0) {
            platform.container.innerHTML = '<div class="empty-state">No messages</div>';
        } else {
            platformMessages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `chat-message ${msg.unread ? 'unread' : ''}`;
                
                // Show original platform for Slack messages
                const platformLabel = (platformName === 'Slack' && msg.platform !== 'Slack') 
                    ? `<span style="font-size: 0.75rem; color: #888; margin-left: 8px;">(${msg.platform})</span>` 
                    : '';
                
                messageDiv.innerHTML = `
                    <div class="chat-header">
                        <span class="chat-sender">${msg.sender}${platformLabel}</span>
                        <span class="chat-time">${formatDate(new Date(msg.timestamp))}</span>
                    </div>
                    <div class="chat-content">${msg.content}</div>
                `;
                
                platform.container.appendChild(messageDiv);
            });
        }
    });
}

// Transform flat message array into structured format matching mock_data.json
// Structure: emails (array), slack (channels), msteams (channels)
// WhatsApp, Instagram, TikTok, Snapchat all go into slack.channels
function transformToStructuredFormat(messages) {
    const structured = {
        emails: [],
        slack: { channels: [] },
        msteams: { channels: [] }
    };
    
    // Group messages by platform
    const platformGroups = {
        'Email': [],
        'WhatsApp': [],
        'Instagram': [],
        'Teams': [],
        'TikTok': [],
        'Snapchat': []
    };
    
    messages.forEach(msg => {
        const platform = msg.platform;
        if (platformGroups[platform]) {
            platformGroups[platform].push(msg);
        }
    });
    
    // Format emails (array format) - matches mock_data.json structure
    structured.emails = platformGroups['Email'].map(msg => ({
        from: `${msg.sender} <${msg.sender.toLowerCase().replace(/\s+/g, '.').replace(/\.+/g, '.')}@example.com>`,
        subject: msg.content.length > 50 ? msg.content.substring(0, 47) + '...' : msg.content,
        timestamp: msg.timestamp,
        body: msg.content
    }));
    
    // Map WhatsApp, Instagram, TikTok, Snapchat to slack.channels
    // Each platform becomes a separate channel in slack
    const slackPlatforms = {
        'WhatsApp': '#whatsapp',
        'Instagram': '#instagram',
        'TikTok': '#tiktok',
        'Snapchat': '#snapchat'
    };
    
    Object.keys(slackPlatforms).forEach(platform => {
        const channelName = slackPlatforms[platform];
        const platformMessages = platformGroups[platform];
        
        if (platformMessages.length > 0) {
            structured.slack.channels.push({
                name: channelName,
                messages: platformMessages.map(msg => ({
                    from: msg.sender,
                    timestamp: msg.timestamp,
                    text: msg.content
                }))
            });
        }
    });
    
    // Map Teams to msteams.channels
    const teamsMessages = platformGroups['Teams'];
    if (teamsMessages.length > 0) {
        // Group Teams messages into channels (use one default channel for now)
        structured.msteams.channels.push({
            name: 'General',
            messages: teamsMessages.map(msg => ({
                from: msg.sender,
                timestamp: msg.timestamp,
                text: msg.content
            }))
        });
    }
    
    return structured;
}

// Export to JSON function - automatically saves to example_chat/example.json
async function exportToJSON(data, filename) {
    // Transform to structured format
    const structuredData = transformToStructuredFormat(data);
    const jsonString = JSON.stringify(structuredData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    
    // Try to use File System Access API for direct save
    if ('showSaveFilePicker' in window) {
        try {
            // Get the parent directory (chat-aggregator-main)
            const fileHandle = await window.showSaveFilePicker({
                suggestedName: filename,
                types: [{
                    description: 'JSON files',
                    accept: { 'application/json': ['.json'] }
                }],
                startIn: 'downloads' // Start in downloads, user can navigate to example_chat
            });
            
            const writable = await fileHandle.createWritable();
            await writable.write(jsonString);
            await writable.close();
            
            // Check if saved to example_chat folder
            const fileName = fileHandle.name;
            const filePath = fileHandle.kind; // Limited info available
            
            alert(`✅ File saved successfully!\n\nFile: ${fileName}\n\nPlease ensure it's saved to: example_chat/example.json`);
            return;
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Error using File System Access API:', err);
                // Fall through to download method
            } else {
                // User cancelled
                return;
            }
        }
    }
    
    // Fallback: Download method (user needs to manually move to example_chat/)
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Show instruction with automation option
    alert('📥 File downloaded!\n\n' +
          'To automate: Run the Python helper script:\n' +
          '  python move_chat_file.py\n\n' +
          'Or manually save to: example_chat/example.json');
}

// Initialize the app
let chatData = [];

function init() {
    // Generate data for all platforms
    chatData = generateChatMessages();
    
    // Display data
    displayChatMessages(chatData);
    
    // Set up single export button for all chats
    document.getElementById('export-all').addEventListener('click', async () => {
        await exportToJSON(chatData, 'example.json');
    });
}

// Run when page loads
document.addEventListener('DOMContentLoaded', init);

