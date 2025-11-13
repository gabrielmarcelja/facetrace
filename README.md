# 🔍 FaceTrace

> **Reverse Face Search CLI Tool** - Find anyone, anywhere

FaceTrace is a powerful command-line tool for reverse face search using advanced facial recognition technology. Simply provide an image and FaceTrace will search across social media platforms to find matching profiles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Features

- 🚀 **Lightning Fast** - Get results in seconds
- 🎯 **High Accuracy** - Advanced facial recognition technology
- 🌐 **Multi-Platform** - Instagram, Facebook, Twitter, OnlyFans, TikTok, LinkedIn, and more
- 🎨 **Beautiful CLI** - Colorful terminal output with progress indicators
- 💳 **Credit System** - 3 free searches, pay-as-you-go with cryptocurrency
- 🔒 **Secure** - Email verification and encrypted API communication
- 💪 **Plug-and-Play** - No complex setup, just clone and run

---

## 📸 Example Output

```
  ███████╗ █████╗  ██████╗███████╗████████╗██████╗  █████╗  ██████╗███████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
  █████╗  ███████║██║     █████╗     ██║   ██████╔╝███████║██║     █████╗
  ██╔══╝  ██╔══██║██║     ██╔══╝     ██║   ██╔══██╗██╔══██║██║     ██╔══╝
  ██║     ██║  ██║╚██████╗███████╗   ██║   ██║  ██║██║  ██║╚██████╗███████╗
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝
           Reverse Face Search - Find anyone, anywhere

[*] Analyzing image: photo.jpg
[*] Uploading to search engine...
[*] Processing faces...
[+] Found 89 matches!

Results:

[+] Instagram    | 95%  | @john_doe        https://instagram.com/john_doe
[+] Facebook     | 92%  | @johndoe         https://facebook.com/johndoe
[+] OnlyFans     | 88%  |                  https://onlyfans.com/johnd
[+] Twitter      | 85%  | @johndoe123      https://twitter.com/johndoe123
[+] TikTok       | 83%  | @johndoe         https://tiktok.com/@johndoe
...

Statistics:
  Total matches: 89
  Avg. similarity: 81.3%
  Top score: 95%

Platforms:
  Instagram: 34
  Facebook: 21
  Twitter: 18
  OnlyFans: 9
  TikTok: 7

[i] Credits remaining: 2
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/gabrielmarcelja/facetrace.git
cd facetrace

# Install dependencies (only 2!)
pip3 install -r requirements.txt
```

### Create Account & Login

```bash
# Register (get 3 free searches!)
python3 facetrace.py register

# Verify your email (check inbox)

# Login
python3 facetrace.py login
```

### Run Your First Search

```bash
# Search by image file
python3 facetrace.py photo.jpg

# Search by image URL
python3 facetrace.py https://example.com/photo.jpg
```

That's it! No API keys to manage, no configuration files. Just works.

---

## 📖 Usage

### Authentication Commands

```bash
# Register new account (get 3 free searches)
python3 facetrace.py register

# Login to your account
python3 facetrace.py login

# Logout (clear credentials)
python3 facetrace.py logout

# Check credit balance
python3 facetrace.py --balance

# Add credits (opens payment page)
python3 facetrace.py --add-credits 10
```

### Search Commands

```bash
# Basic search (file or URL)
python3 facetrace.py image.jpg
python3 facetrace.py https://example.com/photo.jpg

# Set minimum similarity score (70-100)
python3 facetrace.py image.jpg --min-score 85

# Filter by specific platform
python3 facetrace.py photo.png --platform instagram

# Open top matches in browser
python3 facetrace.py suspect.jpg --open

# Export results to JSON
python3 facetrace.py target.jpg --output results.json

# Export to CSV
python3 facetrace.py person.png --output matches.csv

# Open top 10 matches in browser
python3 facetrace.py image.jpg --open --top 10
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `register` | Create new account | - |
| `login` | Login to account | - |
| `logout` | Logout and clear credentials | - |
| `--balance` | Check credit balance | - |
| `--add-credits N` | Purchase N credits (min 10) | - |
| `image` | Path to image file or URL | *Required* |
| `--min-score N` | Minimum similarity score (70-100) | 70 |
| `--platform NAME` | Filter by platform name | None |
| `--open` | Open top matches in browser | False |
| `--output FILE` | Export results (.json or .csv) | None |
| `--top N` | Number of matches to open (requires --open) | 5 |

---

## 🔬 How It Works

FaceTrace uses cloud-based facial recognition technology:

1. **Upload Image** - Send your image securely to FaceTrace API
2. **Face Detection** - Automatically detect and analyze faces
3. **Database Search** - Query 900M+ indexed social media profiles
4. **Return Matches** - Display matching profiles with similarity scores

All processing happens in the cloud via secure HTTPS connection.

---

## 🎯 Use Cases

### OSINT Investigations
- Find social media profiles of persons of interest
- Locate individuals across multiple platforms
- Verify online identities

### Missing Persons
- Search for missing individuals online
- Track digital footprints across platforms

### Security Research
- Profile identification and verification
- Background checks and due diligence

### Journalism
- Verify sources and identities
- Investigate public figures

---

## 🛠️ Technical Details

### Supported Platforms

- Instagram
- Facebook
- Twitter / X
- LinkedIn
- OnlyFans
- TikTok
- VKontakte
- Reddit
- Pinterest
- Tumblr
- YouTube
- Snapchat
- And many more...

### Supported Image Formats

- **Image Files**: JPEG, JPG, PNG, BMP, TIFF, WebP
- **Image URLs**: Direct image links supported

### Requirements

- Python 3.8 or higher
- Internet connection
- Modern operating system (Windows, macOS, Linux)
- Valid email address for registration

### Anti-Abuse Measures

- Email verification required
- Rate limiting (20 searches per hour)
- Temporary email domains blocked
- Credit deduction before search

---

## 📊 Performance

- **Search Speed**: 10-30 seconds per image
- **Accuracy**: Up to 95% similarity matching
- **Database Size**: 900M+ indexed profiles
- **Platforms**: 50+ social media networks
- **API Uptime**: 99.9%

---

## 🔒 Privacy & Ethics

### Privacy Considerations

- FaceTrace is intended for **legal and ethical use only**
- Always respect privacy laws and regulations
- Obtain proper authorization before conducting searches
- Use responsibly for legitimate purposes only

### Ethical Guidelines

- ✅ DO use for OSINT investigations with proper authorization
- ✅ DO use for finding missing persons
- ✅ DO use for security research and verification
- ❌ DON'T use for harassment or stalking
- ❌ DON'T violate privacy laws or regulations
- ❌ DON'T use for malicious purposes

### Data Security

- 🔒 HTTPS encrypted communication
- 🔑 Secure API key authentication
- 📧 Email verification required
- 🚫 No image storage (deleted after processing)

---

## 🐛 Troubleshooting

### "Not authenticated" error
```bash
# Make sure you're logged in
python3 facetrace.py login
```

### "Please verify your email" error
Check your email inbox (including spam folder) for verification link.

### "Insufficient credits" error
```bash
# Check balance
python3 facetrace.py --balance

# Add credits
python3 facetrace.py --add-credits 10
```

### "Rate limit exceeded" error
Maximum 20 searches per hour. Wait and try again later.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/gabrielmarcelja/facetrace.git
cd facetrace
pip3 install -r requirements.txt
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub**: [github.com/gabrielmarcelja/facetrace](https://github.com/gabrielmarcelja/facetrace)
- **Support**: [Issues](https://github.com/gabrielmarcelja/facetrace/issues)

---

## ⚠️ Disclaimer

FaceTrace is provided "as is" without warranty of any kind. The developers are not responsible for any misuse of this tool. Always ensure you have proper authorization before conducting searches and comply with all applicable laws and regulations.

---

**Made with ❤️ by the FaceTrace Team**

*Find anyone, anywhere* 🔍
