import numpy as np
from app.utils.paths import SHADER_FOLDER
import glm

class Cube:
    def __init__(self, app):
        # application and application context
        self.app = app
        self.ctx = app.ctx

        self.vbo = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vertex_array_object()

        self.m_model = self.get_model_matrix()

        self.on_init()

    def on_init(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program["m_model"].write(m_model)

    def get_model_matrix(self):
        m_model = glm.mat4()

        return m_model

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vertex_array_object(self):
        buffer_format = "3f"
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, buffer_format, "in_position")]
        )
        return vao

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]
        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]

        vertex_data = self.get_data(vertices, indices)
        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_buffer_object(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)

        return vbo

    def get_shader_program(self, shader_name):
        with open(f"{SHADER_FOLDER}/{shader_name}.vert", "r") as file:
            vertex_shader = file.read()

        with open(f"{SHADER_FOLDER}/{shader_name}.frag", "r") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program
