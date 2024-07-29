from manim import *
from Pattern_Func import *


class SineWaveFrequencyAnimation(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 2, 0.5],  # x-axis range
            y_range=[-1.5, 1.5, 0.5],  # y-axis range
            axis_config={"color": BLUE}
        )
        axes_labels = axes.get_axis_labels(x_label="t", y_label=MathTex("h(t) \\sim 10^{-25}"))

        grid = NumberPlane(
            x_range=[0, 12, 1.5], y_range=[-3, 3, 1.5],
            background_line_style={"stroke_color": LIGHTER_GREY, "stroke_opacity": 0.30}
        )
        # Initial value of f, fdot, alpha, delta
        f = ValueTracker(1)
        fdot  = ValueTracker(0)
        alpha = ValueTracker(0)
        delta = ValueTracker(0)
        # Sine wave function with frequency f
        sine_wave = always_redraw(lambda: axes.plot(
            lambda t: a("H1", alpha.get_value(), delta.get_value(), t) * np.cos(2 * PI * ((f.get_value() * t) + (1/2 * fdot.get_value() * (t ** 2)))) + b("H1", alpha.get_value(), delta.get_value(), t) * np.sin(2 * PI * ((f.get_value() * t) + (1/2 * fdot.get_value() * (t ** 2)))),
            color=YELLOW
        ))

        # Equation label at the bottom of the scene
        equation_label = MathTex(
            "h(t) = F_{+}(\\alpha, \\delta, \\psi; t) h_{+}(t) + F_{\\times}(\\alpha, \\delta, \\psi; t) h_{\\times}(t)"
        ).to_edge(DOWN, buff=0.0)
        
        
       # value_box = SurroundingRectangle(
       # equation_label,
       # color=BLUE,
       # buff=0,
       # fill_opacity=0.01
       # )

        # Frequency display
        f_label = always_redraw(lambda: MathTex(
            f"f = {f.get_value():.2f}"
        ).to_corner(UR))  # Position at the top right corner
        
        # Fdot display
        fdot_label = always_redraw(lambda: MathTex(
            f"\\dot{{f}} = {fdot.get_value():.2f}"  # Corrected LaTeX formatting
        ).next_to(f_label, DOWN, buff=0.1))  # Position below f_label with some buffer

        # Alpha display
        alpha_label = always_redraw(lambda: MathTex(
            f"\\alpha = {alpha.get_value():.2f}"  # Corrected LaTeX formatting
        ).next_to(fdot_label, DOWN, buff=0.1))  # Position below fdot_label with some buffer

        # Delta display
        delta_label = always_redraw(lambda: MathTex(
            f"\\delta = {delta.get_value():.2f}"  # Corrected LaTeX formatting
        ).next_to(alpha_label, DOWN, buff=0.1))  # Position below fdot_label with some buffer
        
        # Add axes, labels, and sine wave to the scene
        self.add(axes, axes_labels, grid, sine_wave, f_label, fdot_label, alpha_label, delta_label, equation_label)
        
        # Animate change in frequency
        self.play(f.animate.set_value(5), run_time=5, rate_func=there_and_back)  # Animate f
        self.wait()
        self.play(fdot.animate.set_value(-0.5), run_time=5, rate_func=there_and_back)  # Animate fdot
        self.wait()
        self.play(alpha.animate.set_value(2*PI), run_time=10, rate_func=smooth)  # Animate alpha
        self.wait()
        self.play(delta.animate.set_value(PI/2), run_time=5, rate_func=smooth)  # Animate delta
        self.wait()

# To run this code, save it to a file called sine_wave.py and run:
# manim -pql sine_wave.py SineWaveFrequencyAnimation

