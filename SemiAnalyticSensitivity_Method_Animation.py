from SearchFunctions import normed2Fpdf #type: ignore
from SearchFunctions import Sig_2F  # type: ignore
from manim import *
import numpy as np

class Normed2FpdfPlot(Scene):
    def construct(self):
        # Set the range of avg_2Fs for the x-axis
        avg_2Fs_range = np.linspace(5, 10, 400)

        # Create axes
        axes = Axes(
            x_range=[5, 10, 1],  # Adjusted x_range to match data range
            y_range=[0, 0.1, 0.01],
            axis_config={"color": BLUE},
        ).add_coordinates()

        axes_labels = axes.get_axis_labels(x_label="\\langle2\\mathcal{F}\\rangle", y_label="pdf")

        # Add grid
        grid = NumberPlane(
            x_range=[2, 14, 1],  # Match x_range with axes
            y_range=[2, 8, 1],  # Match y_range with axes
            background_line_style={"stroke_color": LIGHT_GREY, "stroke_opacity": 0.3}
        )

        # Initial parameters
        nTemplates_tracker = ValueTracker(10**10)
        nSeg_tracker = ValueTracker(50)

        # Create the initial plot
        avg_2Fs_values = avg_2Fs_range
        plot1 = always_redraw(lambda: axes.plot_line_graph(
            avg_2Fs_values, 
            normed2Fpdf(avg_2Fs_values, nTemplates_tracker.get_value(), nSeg_tracker.get_value()), 
            line_color=YELLOW,
            vertex_dot_radius=False
        ))

        # Create labels for nTemplates and nSeg values
        template_label = always_redraw(lambda: MathTex(
            f"Nt = {nTemplates_tracker.get_value():.0e}",
            font_size=26
        ).to_corner(UP + RIGHT))

        seg_label = always_redraw(lambda: MathTex(
            f"Ns = {nSeg_tracker.get_value():.0f}",
            font_size=26
        ).next_to(template_label, DOWN, buff=0.1))

        param_labels = VGroup(template_label, seg_label)
        value_box = SurroundingRectangle(param_labels, color=WHITE)

        # Add LaTeX equation at the top middle
        latex_equation_1 = MathTex(
            "P(2\\mathcal{F}_{max}) = N_{\\text{s}} N_{\\text{t}} (\\chi^2_{\\text{pdf}}(4N_{\\text{s}})) \\left(\\chi^2_{\\text{cdf}}(4N_{\\text{s}})\\right)^{N_{\\text{t}} - 1}",
            color=YELLOW,
            font_size=26
        ).to_edge(UP)

        # Add everything to the scene
        self.add(axes, axes_labels, plot1, param_labels, value_box, latex_equation_1, grid)

        # Animation to change nSeg from 50 to 80
        self.play(
            nSeg_tracker.animate.set_value(80),
            run_time=5,
            rate_func=linear
        )

        self.wait(1)

        # Animation to change nTemplates from 10^10 to 10^14
        self.play(
            nTemplates_tracker.animate.set_value(10**14),
            run_time=5,
            rate_func=smooth
        )

        self.wait(2)
        self.remove(latex_equation_1)
         
        latex_equation_2 = MathTex(
            "P(2\\mathcal{F}_{sig}) = \\chi^2_{pdf}(4N_{s}, \\rho^{2})",
            color=RED,
            font_size=26
        ).to_edge(UP)

        rho_equation = MathTex(
            "\\rho = \\frac{2}{5}D^{-1}R(\\theta)\sqrt{T_{data}}",
            color=RED,
            font_size=26
        ).next_to(latex_equation_2, DOWN, buff=0.1)


        rho_tracker = ValueTracker(200)

        # Create next plot
        plot2 = always_redraw(lambda: axes.plot_line_graph(
            avg_2Fs_values, 
            Sig_2F(avg_2Fs_values, 80, rho_tracker.get_value()), 
            line_color=RED,
            vertex_dot_radius=False
        ))

        # Add the second plot to the scene
        self.add(plot2, latex_equation_2, rho_equation)
        self.wait(6)
        
        # Animation to change rho from 600 to 800
        self.play(
            rho_tracker.animate.set_value(382),
            run_time=5,
            rate_func=linear
        )

        self.wait(2)

        Depth_value = MathTex(
            "D = 85",
            color=RED,
            font_size=26
        ).next_to(param_labels, DOWN, buff=0.4)

        Depth_box = SurroundingRectangle(Depth_value, color=RED)

        self.add(Depth_value, Depth_box)

        self.wait(3)

        weights = normed2Fpdf(avg_2Fs_range, 1e14, 80)
        weights = weights / np.sum(weights)
        for i in range(10):
            noise_val = np.random.choice(avg_2Fs_range, 1, p=weights)[0]
            sig_val = np.random.noncentral_chisquare(4*80, 382)/80
            noise_part = MathTex(f"{noise_val:.2f}", font_size=26, color=YELLOW).to_edge(RIGHT, buff=6)
            middle_part = MathTex("<", font_size=26).next_to(noise_part, RIGHT, buff=0.2)
            sig_part = MathTex(f"{sig_val:.2f}", font_size=26, color=RED).next_to(middle_part, RIGHT, buff=0.2)
            delta_m_part = MathTex("* \\Delta M?", font_size=26).next_to(sig_part, RIGHT, buff=0.2)
            temp_eq = VGroup(noise_part, middle_part, sig_part, delta_m_part)
            self.add(temp_eq)
            self.wait(5)
            self.remove(temp_eq)
            

# Save this file and run it with the following command:
# manim -pql plot_normed2Fpdf.py Normed2FpdfPlot
