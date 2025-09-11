"""
Pixel Fold specific optimizations for Book of Shadows - The Crone
"""

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

class PixelFoldOptimizer:
    """Optimizations specifically for Google Pixel Fold."""
    
    def __init__(self):
        self.is_folded = True
        self.screen_width = 0
        self.screen_height = 0
        self.fold_threshold = 1.3  # Aspect ratio threshold
        
    def detect_fold_state(self):
        """Detect if Pixel Fold is folded or unfolded."""
        width, height = Window.size
        self.screen_width = width
        self.screen_height = height
        
        # Pixel Fold specs:
        # Folded: 6.2" display (1080 x 2092)
        # Unfolded: 7.6" display (2208 x 1840)
        aspect_ratio = width / height if height > 0 else 1
        
        self.is_folded = aspect_ratio < self.fold_threshold
        return self.is_folded
    
    def get_optimal_layout_params(self):
        """Get optimal layout parameters for current fold state."""
        if self.is_folded:
            return self._get_folded_params()
        else:
            return self._get_unfolded_params()
    
    def _get_folded_params(self):
        """Parameters for folded state."""
        return {
            'nav_height': dp(56),
            'button_height': dp(48),
            'card_padding': dp(16),
            'content_spacing': dp(8),
            'font_size_small': dp(14),
            'font_size_medium': dp(16),
            'font_size_large': dp(18),
            'fab_size': dp(56),
            'dialog_width': 0.9,
            'dialog_height': 0.8
        }
    
    def _get_unfolded_params(self):
        """Parameters for unfolded state."""
        return {
            'nav_height': dp(48),
            'button_height': dp(44),
            'card_padding': dp(20),
            'content_spacing': dp(12),
            'font_size_small': dp(16),
            'font_size_medium': dp(18),
            'font_size_large': dp(20),
            'fab_size': dp(64),
            'dialog_width': 0.7,
            'dialog_height': 0.6
        }
    
    def optimize_for_foldable(self, widget):
        """Apply foldable optimizations to a widget."""
        params = self.get_optimal_layout_params()
        
        # Apply optimizations based on widget type
        if hasattr(widget, 'height') and 'nav' in str(type(widget)).lower():
            widget.height = params['nav_height']
        
        if hasattr(widget, 'font_size'):
            if hasattr(widget, 'bold') and widget.bold:
                widget.font_size = params['font_size_large']
            else:
                widget.font_size = params['font_size_medium']
        
        return widget
    
    def get_adaptive_grid_columns(self):
        """Get optimal number of grid columns for current state."""
        if self.is_folded:
            return 2  # Standard mobile grid
        else:
            return 3  # More columns for unfolded state
    
    def get_optimal_card_height(self):
        """Get optimal card height for current state."""
        if self.is_folded:
            return dp(120)
        else:
            return dp(100)  # Slightly smaller for unfolded
    
    def should_use_landscape_layout(self):
        """Determine if landscape layout should be used."""
        return not self.is_folded and self.screen_width > self.screen_height

# Global instance
pixel_fold_optimizer = PixelFoldOptimizer()