# I Quit — Scoreboard

A colorful, mobile-first scoreboard app for the "I Quit" card game with real-time updates, user authentication, and DynamoDB persistence.

## Features

- 🔐 **User Authentication** - Login/register with session management
- 🎮 **Game Management** - Create games with custom targets (auto-expire after 5 days)
- 👑 **Admin Panel** - Full control: manage games, users, rounds
- 👥 **Player Management** - Bulk add players (comma-separated), admin can remove players
- 🎯 **Round System** - Create/delete rounds, lock/unlock, auto-end when locked
- 🏆 **Live Leaderboard** - Real-time ranking, OUT players sorted by timestamp
- 📺 **Live View** - Read-only spectator link with auto-refresh (10s)
- 📊 **Active/Out Counts** - Visible on main view and live view
- 🎊 **Winner Popup** - Celebration modal when all players are OUT
- 📱 **Mobile-Optimized** - ± button for negative scores, responsive design
- 🔒 **Security** - Password change, user activation/deactivation
- ⏰ **Auto Expiration** - Games expire after 5 days (no new rounds)
- 🎨 **Beautiful UI** - Colorful gradients and smooth animations

## Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: HTMX + Tailwind CSS
- **Database**: AWS DynamoDB (PAY_PER_REQUEST)
- **Auth**: bcrypt password hashing + session tokens
- **Deployment**: Gunicorn + Nginx on EC2

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create tables and admin user
python setup_db.py

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Default Admin**: username `admin`, password `xxx` (change immediately!)

## Admin Features

- View/delete all games and users
- Delete rounds from any game
- Activate/deactivate user accounts
- Remove players and their scores
- Admin users cannot be deleted/deactivated

## Game Rules

- Target score (default: 150)
- Add positive/negative deltas each round
- Players ≥ target score are OUT
- Winner = last IN player (survives longest)
- OUT players ranked by who stayed in longest
- Games expire after 5 days

## Recent Bug Fixes

- ✅ Winner popup now shows the last IN player (correct winner logic)
- ✅ OUT players ranked by who stayed in longest (not by score)
- ✅ User activation/deactivation error message displays correctly on login
- ✅ Game expiration enforced (5 days - no new rounds)
- ✅ Admin controls for deleting users and rounds
- ✅ Live view shows Active/Out player counts
- ✅ Phone number formatting fixed (+971 56 8103175)

## Developer

💻 **Aziz Zoaib**

MIT
