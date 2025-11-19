from PIL import Image, ImageDraw, ImageFont

# Create architecture diagram for StackSpot Agent API
img = Image.new('RGB', (1200, 800), 'white')
draw = ImageDraw.Draw(img)

# Colors
blue = '#4A90E2'
green = '#7ED321'
orange = '#F5A623'
red = '#D0021B'
gray = '#9B9B9B'

# External Systems
draw.rectangle([50, 50, 200, 100], outline=orange, fill='#FFF2CC', width=2)
draw.text((125, 75), 'StackSpot APIs', fill='black', anchor='mm')

# Main Application Layer
draw.rectangle([300, 150, 900, 650], outline=blue, fill='#E6F3FF', width=3)
draw.text((600, 130), 'StackSpot Agent API', fill=blue, anchor='mm')

# Agents Layer
draw.rectangle([320, 180, 580, 280], outline=green, fill='#F0FFF0', width=2)
draw.text((450, 200), 'Agents Layer', fill=green, anchor='mm')
draw.rectangle([330, 220, 470, 260], outline='black', fill='white')
draw.text((400, 240), 'StackSpotAgent', fill='black', anchor='mm')
draw.rectangle([480, 220, 570, 260], outline='black', fill='white')
draw.text((525, 240), 'AgentChat', fill='black', anchor='mm')

# Models Layer
draw.rectangle([320, 300, 580, 400], outline=red, fill='#FFF0F0', width=2)
draw.text((450, 320), 'Models Layer', fill=red, anchor='mm')
draw.rectangle([330, 340, 420, 380], outline='black', fill='white')
draw.text((375, 360), 'LLMConfig', fill='black', anchor='mm')
draw.rectangle([430, 340, 520, 380], outline='black', fill='white')
draw.text((475, 360), 'PromptConfig', fill='black', anchor='mm')
draw.rectangle([530, 340, 570, 380], outline='black', fill='white')
draw.text((550, 360), 'Session', fill='black', anchor='mm')

# Utils Layer
draw.rectangle([320, 420, 580, 520], outline=gray, fill='#F5F5F5', width=2)
draw.text((450, 440), 'Utils Layer', fill=gray, anchor='mm')
draw.rectangle([330, 460, 420, 500], outline='black', fill='white')
draw.text((375, 480), 'APIClient', fill='black', anchor='mm')
draw.rectangle([430, 460, 520, 500], outline='black', fill='white')
draw.text((475, 480), 'FileUploader', fill='black', anchor='mm')
draw.rectangle([530, 460, 570, 500], outline='black', fill='white')
draw.text((550, 480), 'URLUtils', fill='black', anchor='mm')

# Config Layer
draw.rectangle([320, 540, 580, 620], outline='purple', fill='#F0F0FF', width=2)
draw.text((450, 560), 'Config Layer', fill='purple', anchor='mm')
draw.rectangle([330, 580, 420, 610], outline='black', fill='white')
draw.text((375, 595), 'Dynaconf', fill='black', anchor='mm')
draw.rectangle([430, 580, 520, 610], outline='black', fill='white')
draw.text((475, 595), 'Logger', fill='black', anchor='mm')
draw.rectangle([530, 580, 570, 610], outline='black', fill='white')
draw.text((550, 595), 'Settings', fill='black', anchor='mm')

# Web Interface
draw.rectangle([620, 180, 880, 280], outline='#FF6B35', fill='#FFF5F0', width=2)
draw.text((750, 200), 'Web Interface', fill='#FF6B35', anchor='mm')
draw.rectangle([630, 220, 720, 260], outline='black', fill='white')
draw.text((675, 240), 'Chainlit App', fill='black', anchor='mm')
draw.rectangle([730, 220, 870, 260], outline='black', fill='white')
draw.text((800, 240), 'File Management', fill='black', anchor='mm')

# Examples & Tests
draw.rectangle([620, 300, 880, 400], outline='#50C878', fill='#F0FFF8', width=2)
draw.text((750, 320), 'Examples & Tests', fill='#50C878', anchor='mm')
draw.rectangle([630, 340, 720, 380], outline='black', fill='white')
draw.text((675, 360), 'Examples', fill='black', anchor='mm')
draw.rectangle([730, 340, 870, 380], outline='black', fill='white')
draw.text((800, 360), 'Unit Tests', fill='black', anchor='mm')

# Storage
draw.rectangle([950, 300, 1150, 500], outline='#8B4513', fill='#FFF8DC', width=2)
draw.text((1050, 320), 'Storage', fill='#8B4513', anchor='mm')
draw.rectangle([960, 350, 1040, 390], outline='black', fill='white')
draw.text((1000, 370), 'Logs', fill='black', anchor='mm')
draw.rectangle([1050, 350, 1140, 390], outline='black', fill='white')
draw.text((1095, 370), 'Uploads', fill='black', anchor='mm')
draw.rectangle([960, 410, 1040, 450], outline='black', fill='white')
draw.text((1000, 430), 'Files', fill='black', anchor='mm')
draw.rectangle([1050, 410, 1140, 450], outline='black', fill='white')
draw.text((1095, 430), 'Config', fill='black', anchor='mm')

# Arrows - External to Internal
draw.line([200, 75, 300, 230], fill='black', width=2)
draw.polygon([(295, 225), (305, 230), (295, 235)], fill='black')

# Internal connections
draw.line([450, 280, 450, 300], fill='black', width=2)
draw.line([450, 400, 450, 420], fill='black', width=2)
draw.line([450, 520, 450, 540], fill='black', width=2)

# Web to Core
draw.line([620, 230, 580, 230], fill='black', width=2)

# Storage connections
draw.line([580, 480, 950, 400], fill='black', width=2)

# Title
draw.text((600, 30), 'StackSpot Agent API - Arquitetura do Sistema', fill='black', anchor='mm')

# Legend
draw.rectangle([50, 700, 400, 780], outline='black', fill='#F9F9F9')
draw.text((60, 710), 'Legenda:', fill='black')
draw.text((60, 730), '• Agents: Gerenciamento de agentes IA', fill='black')
draw.text((60, 745), '• Models: Configurações e sessões', fill='black')
draw.text((60, 760), '• Utils: Utilitários e clientes API', fill='black')

img.save('stackspot_architecture_diagram.png')
print('Diagrama de arquitetura salvo como stackspot_architecture_diagram.png')