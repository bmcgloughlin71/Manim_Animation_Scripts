from manim import *

class FourDimensionalGrid(Scene):
    def construct(self):
        # Define the screen dimensions
        screen_width = config["frame_width"]
        screen_height = config["frame_height"]

        # Calculate the size and position of the grids
        grid_width = screen_width / 2 - 1.5  # Subtract 1 for padding
        grid_height = screen_height / 2 - 1.5  # Subtract 1 for padding
        grid1_position = np.array([-screen_width / 4, -screen_height / 4 + 2, 0])
        grid2_position = np.array([screen_width / 4, -screen_height / 4 + 2, 0])

        # Create the first 2D grid (lines)
        grid1_lines = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": False},
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        ).scale(grid_width / 10).move_to(grid1_position)

        # Create the grid points for the first grid (aligned with nodes)
        grid1_points = VGroup(*[Dot(color=BLUE).move_to(grid1_lines.coords_to_point(x, y)) for x in range(-5, 6) for y in range(-5, 6)])

        # Create the second 2D grid (lines)
        grid2_lines = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": False},
            background_line_style={
                "stroke_color": GREEN,
                "stroke_width": 2,
                "stroke_opacity": 0.5
            }
        ).scale(grid_width / 10).move_to(grid2_position)

        # Create the grid points for the second grid (aligned with nodes)
        grid2_points = VGroup(*[Dot(color=BLUE).move_to(grid2_lines.coords_to_point(x, y)) for x in range(-5, 6) for y in range(-5, 6)])

        # Create axis labels for the first grid
        grid1_x_label = MathTex("f").next_to(grid1_lines.get_x_axis(), RIGHT)
        grid1_y_label = MathTex("\\dot{f}").next_to(grid1_lines.get_y_axis(), UP)

        # Create axis labels for the second grid
        grid2_x_label = MathTex("\\alpha").next_to(grid2_lines.get_x_axis(), RIGHT)
        grid2_y_label = MathTex("\\delta").next_to(grid2_lines.get_y_axis(), UP)

        # Create and add the yellow "x" for the first grid
        yellow_x1 = Cross(stroke_color=YELLOW, stroke_width=3).scale(0.2).move_to(grid1_lines.coords_to_point(-3.1, 3.1))
        nearest_node1 = Dot(color=ORANGE).move_to(grid1_lines.coords_to_point(-3, 3))

        # Create and add the yellow "x" for the second grid
        yellow_x2 = Cross(stroke_color=YELLOW, stroke_width=3).scale(0.2).move_to(grid2_lines.coords_to_point(3.1, -3.1))
        nearest_node2 = Dot(color=ORANGE).move_to(grid2_lines.coords_to_point(3, -3))

        # Display the first grid (lines), grid points, and axis labels together
        self.play(Create(grid1_lines), Create(grid1_points), Write(grid1_x_label), Write(grid1_y_label), run_time=5)

          # Pause to view the first grid

        # Display the second grid (lines), grid points, and axis labels together
        self.play(Create(grid2_lines), Create(grid2_points), Write(grid2_x_label), Write(grid2_y_label), run_time=5)
        
        self.wait(12)

        self.play(Create(yellow_x1), Create(nearest_node1))
        self.play(Create(yellow_x2), Create(nearest_node2))

        self.wait(12)  # Pause to view the second grid
        self.remove(yellow_x1, nearest_node1)
        self.remove(yellow_x2, nearest_node2)

        # Function to add yellow cross and nearest orange dot on grid 1

        def add_yellow_cross_and_orange_dot_on_grids(x, y, x2, y2, delta, delta2):
            yellow_cross = Cross(stroke_color=YELLOW, stroke_width=3).scale(0.2).move_to(grid1_lines.coords_to_point(x+delta, y+delta))
            yellow_cross2 = Cross(stroke_color=YELLOW, stroke_width=3).scale(0.2).move_to(grid2_lines.coords_to_point(x+delta2, y+delta2))
            orange_dot = Dot(color=ORANGE).move_to(grid1_lines.coords_to_point(x, y))
            orange_dot2 = Dot(color=ORANGE).move_to(grid2_lines.coords_to_point(x, y))
            self.play(Create(yellow_cross), Create(orange_dot), Create(yellow_cross2), Create(orange_dot2))
            self.wait(1)
            self.remove(yellow_cross, yellow_cross2, orange_dot, orange_dot2)

        

        # Example: Add more pairs on grid 1 and grid 2 sequentially
        add_yellow_cross_and_orange_dot_on_grids(-2, 4, 1, 1, 0.1, -0.2)
        add_yellow_cross_and_orange_dot_on_grids(1, -2, 2, -4, 0.2, 0.34)
        add_yellow_cross_and_orange_dot_on_grids(0, 0, 1, 3, 0.1, 0.05)
        add_yellow_cross_and_orange_dot_on_grids(-3, 3, 4, 4, 0.01, 0.1)

        self.wait(2)  # Pause at the end

