"""User Guide Dialog"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class UserGuideDialog(Adw.Window):
    """Display user guide for the Eisenhower Matrix"""
    
    def __init__(self, parent):
        super().__init__()
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(900, 700)
        self.set_title("How to Use the Eisenhower Matrix")
        
        # Main container
        toolbar_view = Adw.ToolbarView()
        
        # Header bar
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        # Content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        
        # Clamp for better reading
        clamp = Adw.Clamp()
        clamp.set_maximum_size(800)
        clamp.set_tightening_threshold(600)
        
        # Main content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        
        # Introduction
        intro_box = self._create_section(
            "Understanding the Eisenhower Matrix",
            "The Eisenhower Matrix is a time management framework that helps you prioritize tasks by urgency and importance. Named after President Dwight D. Eisenhower, who said: \"What is important is seldom urgent and what is urgent is seldom important.\""
        )
        content_box.append(intro_box)
        
        # The Four Quadrants
        quadrants_title = Gtk.Label()
        quadrants_title.set_markup("<span size='x-large' weight='bold'>The Four Quadrants</span>")
        quadrants_title.set_xalign(0)
        content_box.append(quadrants_title)
        
        # Q1
        q1_box = self._create_quadrant_section(
            "Quadrant 1: Urgent & Important",
            "Do First 🔴",
            [
                "<b>What belongs here:</b> Crises, emergencies, deadline-driven projects, problems requiring immediate attention",
                "<b>Examples:</b> Production system down, client emergency, critical bug, overdue deadline, medical emergency",
                "<b>Strategy:</b> Do these immediately. However, living in Q1 means you're always in crisis mode.",
                "<b>Warning:</b> If 80% of your tasks are here, you're not being selective enough or planning ahead."
            ]
        )
        content_box.append(q1_box)
        
        # Q2
        q2_box = self._create_quadrant_section(
            "Quadrant 2: Important, Not Urgent",
            "Schedule 🟡",
            [
                "<b>What belongs here:</b> Long-term strategic planning, prevention, relationship building, personal development",
                "<b>Examples:</b> Strategic planning, learning new skills, exercise, building relationships, process improvements",
                "<b>Strategy:</b> This is the MOST IMPORTANT quadrant! Schedule dedicated time for these activities.",
                "<b>Success tip:</b> Spend 50-65% of your time here to prevent Q1 crises and build for the future."
            ]
        )
        content_box.append(q2_box)
        
        # Q3
        q3_box = self._create_quadrant_section(
            "Quadrant 3: Urgent, Not Important",
            "Delegate 🔵",
            [
                "<b>What belongs here:</b> Interruptions that seem urgent but don't align with your goals, other people's priorities",
                "<b>Examples:</b> Most emails and phone calls, many meetings, routine reports, administrative tasks",
                "<b>Strategy:</b> Delegate when possible. Batch them together if you can't delegate.",
                "<b>Key question:</b> Does this task align with my core responsibilities, or can someone else handle it?"
            ]
        )
        content_box.append(q3_box)
        
        # Q4
        q4_box = self._create_quadrant_section(
            "Quadrant 4: Not Urgent, Not Important",
            "Eliminate 🟢",
            [
                "<b>What belongs here:</b> Time-wasters, distractions, busy work with no real value",
                "<b>Examples:</b> Excessive social media, mindless web surfing, watching TV for hours, unnecessary shopping",
                "<b>Strategy:</b> Minimize or eliminate. Some relaxation is healthy, but don't let Q4 dominate your time.",
                "<b>Healthy approach:</b> Schedule intentional breaks instead of mindless scrolling."
            ]
        )
        content_box.append(q4_box)
        
        # Getting Started
        getting_started = self._create_expandable_section(
            "Getting Started with This App",
            [
                ("1. Brain Dump", "Add all your tasks without worrying about perfect categorization. Click 'Add Task' in any quadrant."),
                ("2. Categorize", "Ask two questions: Is this urgent? Is this important? Move tasks to the right quadrant."),
                ("3. Add Due Dates", "Click the calendar icon when editing tasks. Quick buttons: Today, Tomorrow. Color-coded: 🔴 Overdue, 🟠 Due Soon, ⚪ Future"),
                ("4. Enrich with Context", "Add Notes for context, Tags for categories (e.g., 'client-work', 'quick-win'), and Metadata for extra info."),
                ("5. Daily Review", "Morning: Review Q1, schedule Q2. Throughout: Add new tasks, mark completed. Evening: Plan tomorrow.")
            ]
        )
        content_box.append(getting_started)
        
        # App Features
        features = self._create_expandable_section(
            "Key Features",
            [
                ("🔍 Search", "Press Ctrl+F or click the search icon. Search across all quadrants by description, notes, or tags."),
                ("📁 Projects", "Click the folder icon to manage multiple projects. Separate contexts: Work, Personal, Side Projects."),
                ("📅 Due Dates", "Visual indicators: Red (overdue), Orange (due within 3 days), Gray (future dates)."),
                ("⌨️  Keyboard Shortcuts", "Ctrl+Q (Quit), Ctrl+1-4 (Focus quadrant), Ctrl+E (Export), Ctrl+T (Theme). See full list in Help > Keyboard Shortcuts."),
                ("📤 Export/Import", "Menu > Export: JSON, CSV, Markdown, Calendar. Import from other tools or back up regularly."),
                ("🎨 Theme Toggle", "Click the moon/sun icon or press Ctrl+T to switch between light and dark themes.")
            ]
        )
        content_box.append(features)
        
        # Best Practices
        practices = self._create_expandable_section(
            "Best Practices",
            [
                ("Review Daily", "Start each day with a 5-10 minute review. Plan Q2 time blocks, handle Q1 items."),
                ("Focus on Q2", "This is where success happens. Prevention beats firefighting. Schedule Q2 time as non-negotiable appointments."),
                ("The 2-Minute Rule", "If it takes less than 2 minutes, do it now instead of adding it to the matrix."),
                ("Be Honest", "Don't let everything be 'urgent' or 'important'. Ask: What happens if this waits until tomorrow?"),
                ("Batch Q3 Tasks", "Group similar Q3 tasks (emails, admin work) into dedicated time blocks."),
                ("Weekly Review", "Every week: Review completed tasks, analyze patterns, plan Q2 initiatives, prune Q4 tasks.")
            ]
        )
        content_box.append(practices)
        
        # Common Mistakes
        mistakes = self._create_expandable_section(
            "Common Mistakes to Avoid",
            [
                ("❌ Everything in Q1", "If 80% of tasks are urgent & important, you're not planning ahead. Spend more time in Q2 to prevent crises."),
                ("❌ Ignoring Q2", "Q2 prevents Q1 fires. If you never have time for Q2, you'll always be firefighting."),
                ("❌ No Daily Review", "An unmaintained matrix becomes clutter. Set a 5-minute daily review as part of your routine."),
                ("❌ Too Rigid", "Priorities change. It's okay to move tasks between quadrants. Use judgment."),
                ("❌ Confusing Urgent/Important", "Urgent = time-sensitive. Important = value-aligned. Just because someone wants it urgently doesn't make it important to YOUR goals.")
            ]
        )
        content_box.append(mistakes)
        
        # Success Indicators
        success = self._create_section(
            "Measuring Success",
            "Track these patterns over time:\n\n"
            "✅ <b>Healthy Matrix:</b> 50-65% time in Q2, Q1 decreasing, Q3 delegated/batched, Q4 minimal\n\n"
            "❌ <b>Unhealthy Matrix:</b> Living in Q1 (crisis mode), no Q2 (no strategic work), Q3 dominates, Q4 is your stress escape\n\n"
            "<b>Monthly Review Questions:</b>\n"
            "• Am I spending more time preventing crises (Q2)?\n"
            "• Which Q1 tasks could have been prevented with Q2 work?\n"
            "• What Q3 tasks can I delegate or eliminate?\n"
            "• Am I protecting time for what truly matters?"
        )
        content_box.append(success)
        
        clamp.set_child(content_box)
        scrolled.set_child(clamp)
        toolbar_view.set_content(scrolled)
        
        self.set_content(toolbar_view)
    
    def _create_section(self, title, description):
        """Create a simple text section"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_wrap(True)
        box.append(title_label)
        
        desc_label = Gtk.Label()
        desc_label.set_markup(description)
        desc_label.set_xalign(0)
        desc_label.set_wrap(True)
        box.append(desc_label)
        
        return box
    
    def _create_quadrant_section(self, title, subtitle, points):
        """Create a quadrant description section"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        box.append(title_label)
        
        # Subtitle
        subtitle_label = Gtk.Label()
        subtitle_label.set_markup(f"<span style='italic'>{subtitle}</span>")
        subtitle_label.set_xalign(0)
        box.append(subtitle_label)
        
        # Points
        for point in points:
            point_label = Gtk.Label()
            point_label.set_markup(f"• {point}")
            point_label.set_xalign(0)
            point_label.set_wrap(True)
            point_label.set_margin_start(12)
            box.append(point_label)
        
        # Add separator
        separator = Gtk.Separator()
        separator.set_margin_top(8)
        box.append(separator)
        
        return box
    
    def _create_expandable_section(self, title, items):
        """Create an expandable section with title and items"""
        expander = Gtk.Expander()
        expander.set_label(title)
        
        # Make title bold
        label_widget = expander.get_label_widget()
        if label_widget:
            label_widget.set_markup(f"<span weight='bold' size='large'>{title}</span>")
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content_box.set_margin_start(24)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        
        for item_title, item_description in items:
            item_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            
            item_title_label = Gtk.Label()
            item_title_label.set_markup(f"<span weight='bold'>{item_title}</span>")
            item_title_label.set_xalign(0)
            item_box.append(item_title_label)
            
            item_desc_label = Gtk.Label()
            item_desc_label.set_text(item_description)
            item_desc_label.set_xalign(0)
            item_desc_label.set_wrap(True)
            item_desc_label.add_css_class("dim-label")
            item_box.append(item_desc_label)
            
            content_box.append(item_box)
        
        expander.set_child(content_box)
        return expander
