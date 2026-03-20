# I Quit — Scoreboard

A colorful, mobile-first scoreboard app for the "I Quit" card game with real-time updates, user authentication, and DynamoDB persistence.

## Features

- 🔐 **User Authentication** - Login system with session management
- 🎮 **Game Management** - Create and track multiple games (users see only their games)
- 👑 **Admin Panel** - Delete games, manage all users' games
- 👥 **Player Management** - Add players dynamically
- 🎯 **Round System** - Organize scoring by rounds with lock/unlock functionality
- 🏆 **Live Leaderboard** - Real-time ranking with IN/OUT status
- 📺 **Live View** - Share read-only link for spectators
- 📜 **Game History** - View your recent games on homepage
- 🔒 **Round Locking** - Lock rounds to prevent accidental changes
- 🏁 **End Round** - Quickly end and lock rounds
- ↩️ **Undo** - Revert last action
- 🎨 **Beautiful UI** - Colorful gradients and smooth animations
- 📱 **Mobile-First** - Responsive design optimized for phones

## Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: HTMX + Tailwind CSS
- **Database**: AWS DynamoDB (3 tables: games, events, users)
- **Auth**: Passlib (bcrypt) + itsdangerous (session tokens)
- **Deployment**: Uvicorn server

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export AWS_REGION=me-central-1
export GAMES_TABLE=iquit_games
export EVENTS_TABLE=iquit_events
export USERS_TABLE=iquit_users
export SECRET_KEY=your-secret-key-here

# Create database tables and admin user
python setup_db.py

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## First Time Setup

1. Run `python setup_db.py` to create the users table and admin account
2. Login with username: `admin`, password: `admin123`
3. **Important**: Change admin password or create your own account
4. Optionally make your account admin from DynamoDB console

## Usage

1. **Register/Login**: Create account or login
2. **Create a Game**: Set game name and target score
3. **Add Players**: Enter player names
4. **Create Rounds**: Add rounds to organize scoring
5. **Score**: Enter deltas for each player per round (supports negative values)
6. **Track Progress**: Monitor leaderboard in real-time
7. **Share Live View**: Copy live link for spectators
8. **End Round**: Lock rounds when complete
9. **Start New Round**: Scores reset per round

## Admin Features

- View all games from all users
- Delete any game
- Access admin panel from homepage
- Full control over game management

## Game Rules

- Players start at 0 each round
- Add positive/negative deltas to adjust scores
- Players with total ≥ target score are marked "OUT"
- Game ends when all players reach target

## Project Structure

```
iquitscorer/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── db.py            # DynamoDB operations
│   ├── logic.py         # Game logic & calculations
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # JavaScript files
└── requirements.txt     # Python dependencies
```

## Developer

💻 **Developed by Aziz Zoaib**

## License

MIT
