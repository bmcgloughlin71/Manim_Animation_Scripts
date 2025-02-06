from manim import *
from SearchFunctions import *

class GravitationalWavePolarizations(Scene):
    def construct(self):
        h_zero = 0.2
        iota_tracker = ValueTracker(90) #TODO: 
        f_gw = 1  # TODO: fdot implementation
        run_time=20

        
        ## Define three rings of particles ##
        # Plus (+) polarization
        plus_ring = VGroup(*[Dot(point=ORIGIN + np.array([np.cos(theta), np.sin(theta), 0])) 
                        for theta in np.linspace(0, 2 * np.pi, 40)])
        plus_ring.set_color(BLUE)
        
        # Cross (x) polarization
        cross_ring = VGroup(*[Dot(point=ORIGIN + np.array([np.cos(theta), np.sin(theta), 0])) 
                        for theta in np.linspace(0, 2 * np.pi, 40)])
        cross_ring.set_color(RED)

        # Plus and Cross polarizations
        both_ring = VGroup(*[Dot(point=ORIGIN + np.array([np.cos(theta), np.sin(theta), 0])) 
                        for theta in np.linspace(0, 2 * np.pi, 40)])
        both_ring.set_color(PURPLE)
        


        
        

        
        
        ## Setup Scene ##
        self.add(cross_ring)
        cross_ring.to_corner(UP + LEFT)
        cross_text = MathTex(r"\rm\ x \text{ polarisation}").scale(0.5).set_color(RED).next_to(cross_ring, DOWN)
        self.add(cross_text)

        self.add(plus_ring)
        plus_ring.to_corner(UP + RIGHT)
        plus_text = MathTex(r"  \text{+ polarisation}").scale(0.5).set_color(BLUE).next_to(plus_ring, DOWN)
        self.add(plus_text)

        self.add(both_ring)
        both_text = MathTex(r"  \text{Both polarisations}").scale(0.5).set_color(PURPLE).next_to(both_ring, DOWN)
        self.add(both_text)

        iota_display = MathTex(r"\iota =", "0^\circ").scale(0.7).to_edge(DOWN)
        iota_display.add_updater(lambda m: m.become(
            MathTex(r"\iota =", f"{int(iota_tracker.get_value())}^\circ").scale(0.7).to_edge(DOWN)
             ))
        self.add(iota_display)

        # Get the center positions of the rings after they are shifted
        center_cross_ring = cross_ring.get_center()
        center_plus_ring = plus_ring.get_center()
        #center_both_ring = both_ring.get_center()
        
        # Define the original positions of the dots relative to the center of the ring
        original_cross_positions = [dot.get_center() for dot in cross_ring]
        original_plus_positions = [dot.get_center() for dot in plus_ring]
        original_both_positions = [dot.get_center() for dot in both_ring]
        cross_offsets = [dot.get_center() - center_cross_ring for dot in cross_ring]
        plus_offsets = [dot.get_center() - center_plus_ring for dot in plus_ring]



        # Define the deformation functions for "+" and "×" polarizations

        def plus_wave_deformation(mob, t):
            actual_t = t * run_time  # Convert normalized t to real-world time
            current_iota = np.radians(iota_tracker.get_value())
            for i, dot in enumerate(mob):
                # Get the original position of the dot
                x_offset, y_offset, z_offset = plus_offsets[i]
                
                # Apply the deformation to the offsets
                new_x = x_offset * (1 + h_plus(h_zero, current_iota, f_gw, actual_t)) + center_plus_ring[0]
                new_y = y_offset * (1 - h_plus(h_zero, current_iota, f_gw, actual_t)) + center_plus_ring[1]
                
                # Move the dot to the new position
                dot.move_to([new_x, new_y, z_offset])

        def cross_wave_deformation(mob, t):
            actual_t = t * run_time  # Convert normalized t to real-world time
            current_iota = np.radians(iota_tracker.get_value())
            for i, dot in enumerate(mob):
                # Get the original position of the dot
                x_offset, y_offset, z_offset = cross_offsets[i]
                
                # Apply the deformation to the offsets
                new_x = x_offset * 1 + y_offset * h_cross(h_zero, current_iota, f_gw, actual_t) + center_cross_ring[0]
                new_y = y_offset * 1 + x_offset * h_cross(h_zero, current_iota, f_gw, actual_t) + center_cross_ring[1]
                
                # Move the dot to the new position
                dot.move_to([new_x, new_y, z_offset])

        def both_deformations(mob, t):
            actual_t = t * run_time  # Convert normalized t to real-world time
            current_iota = np.radians(iota_tracker.get_value())
            for i, dot in enumerate(mob):
                x, y, z = original_both_positions[i]
                new_x = x + x * h_plus(h_zero, current_iota, f_gw, actual_t) + y * h_cross(h_zero, current_iota, f_gw, actual_t)
                new_y = y + x * h_cross(h_zero, current_iota, f_gw, actual_t) - y * h_plus(h_zero, current_iota, f_gw, actual_t) 

                dot.move_to([new_x, new_y, z])

        # Create animations for the "+" and "×" polarizations
        self.play(UpdateFromAlphaFunc(plus_ring, lambda m, t: plus_wave_deformation(m, t)),
                  UpdateFromAlphaFunc(cross_ring, lambda m, t: cross_wave_deformation(m, t)),
                  UpdateFromAlphaFunc(both_ring, lambda m, t: both_deformations(m, t)),
                 run_time=run_time, rate_func=linear)
        run_time=5
        self.play(iota_tracker.animate.set_value(0),
                  UpdateFromAlphaFunc(plus_ring, lambda m, t: plus_wave_deformation(m, t)),
                  UpdateFromAlphaFunc(cross_ring, lambda m, t: cross_wave_deformation(m, t)),
                  UpdateFromAlphaFunc(both_ring, lambda m, t: both_deformations(m, t)),
                 run_time=run_time, rate_func=linear
                  )
        
        self.play(UpdateFromAlphaFunc(plus_ring, lambda m, t: plus_wave_deformation(m, t)),
                  UpdateFromAlphaFunc(cross_ring, lambda m, t: cross_wave_deformation(m, t)),
                  UpdateFromAlphaFunc(both_ring, lambda m, t: both_deformations(m, t)),
                 run_time=run_time, rate_func=linear
                  )

