"""
Floating GUI - Siri/ChatGPT-style floating window
Always visible, draggable, responds with visual feedback
"""

try:
    from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
    from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
    import sys
    HAS_PYQT = True
except ImportError:
    HAS_PYQT = False


class FloatingAssistantWidget(QWidget):
    """Floating assistant widget - always visible on screen"""
    
    # States
    STATE_IDLE = "IDLE"
    STATE_LISTENING = "LISTENING"
    STATE_PROCESSING = "PROCESSING"
    STATE_SPEAKING = "SPEAKING"
    
    # Colors for states
    STATE_COLORS = {
        STATE_IDLE: "#4A90E2",        # Blue
        STATE_LISTENING: "#50E3C2",   # Green
        STATE_PROCESSING: "#F5A623",  # Orange
        STATE_SPEAKING: "#D0021B",    # Red
    }
    
    def __init__(self):
        super().__init__()
        self.current_state = self.STATE_IDLE
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        
        # Window settings
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Main label (orb/circle)
        self.status_label = QLabel("Jarvis")
        font = QFont("Arial", 14, QFont.Bold)
        self.status_label.setFont(font)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Styling
        self.set_state(self.STATE_IDLE)
        
        # Size & position
        self.resize(150, 150)
        self.move(100, 100)
        
        # Double-click to minimize
        self.double_click_timer = QTimer()
        self.double_click_timer.setSingleShot(True)
        self.double_click_timer.timeout.connect(self.on_click)
        
        self.click_count = 0
    
    def set_state(self, state):
        """Update widget state and appearance"""
        self.current_state = state
        
        color = self.STATE_COLORS.get(state, "#4A90E2")
        
        # Style based on state
        if state == self.STATE_LISTENING:
            self.status_label.setText("🎤 Listening...")
            size = 200
        elif state == self.STATE_PROCESSING:
            self.status_label.setText("⚙️ Processing...")
            size = 180
        elif state == self.STATE_SPEAKING:
            self.status_label.setText("🔊 Speaking...")
            size = 180
        else:  # IDLE
            self.status_label.setText("🔵 Ready")
            size = 150
        
        # Apply color
        stylesheet = f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: {size//2}px;
                padding: 20px;
                font-weight: bold;
            }}
        """
        self.status_label.setStyleSheet(stylesheet)
        self.resize(size, size)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_start = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Handle dragging"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start)
    
    def mouseDoubleClickEvent(self, event):
        """Minimize on double-click"""
        self.hide()
    
    def on_click(self):
        """Handle click"""
        if self.click_count == 0:
            self.click_count = 0


class SimpleFloatingUI:
    """Minimal floating UI (no PyQt dependency)"""
    
    def __init__(self):
        self.state = "ready"
    
    def update_state(self, state):
        """Update UI state"""
        self.state = state
        
        states_display = {
            "ready": "🔵 Ready",
            "listening": "🎤 Listening...",
            "processing": "⚙️ Processing...",
            "speaking": "🔊 Speaking...",
        }
        
        print(f"\r[UI] {states_display.get(state, state):<25}", end="", flush=True)


def create_floating_ui():
    """Factory function to create appropriate UI"""
    
    if HAS_PYQT:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        return FloatingAssistantWidget()
    else:
        return SimpleFloatingUI()


def start_floating_ui():
    """Start floating UI in non-blocking way"""
    
    if not HAS_PYQT:
        print("[INFO] PyQt5 not installed. Using terminal UI.")
        print("[INFO] Install: pip install PyQt5")
        return SimpleFloatingUI()
    
    ui = create_floating_ui()
    ui.show()
    return ui
