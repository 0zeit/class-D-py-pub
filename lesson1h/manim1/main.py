from manim import *

korean = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv"
)
korean.add_to_preamble(r"""
\usepackage{kotex}
\usepackage{fontspec}
\setmainfont{Noto Sans CJK KR}
""")

class SomeManim(Scene):
    def construct(self):
        title = Tex(r"\LaTeX 써보기!", tex_template=korean)
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")

        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex(r"텍스트 애니메이션!", tex_template=korean)
        transform_title.to_corner(UP + LEFT)

        self.play(
            Transform(title, transform_title),
            LaggedStart(*(FadeOut(obj, shift=DOWN) for obj in basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex(r"그리드(격자) 그려보기", tex_template=korean)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(r"비선형 함수를 그리드에 적용하기!", tex_template=korean)
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ],
                ),
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()