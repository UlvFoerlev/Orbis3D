import pygame as pg
import moderngl as mgl
import sys
from app.geometry import Triangle, Cube
from app.camera import Camera

class GraphicsEngine():
    def __init__(self, win_size=(1600, 900)):
        # Init pygame modules
        pg.init()

        # window size
        self.WIN_SIZE=win_size

        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()

        # Timekeeping
        self.clock = pg.time.Clock()
        self.time = 0

        # Camera
        self.camera = Camera(self)

        # scene
        self.scene = Cube(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))

        # render scene
        self.scene.render()

        # swap buffers
        pg.display.flip()

    def update_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.update_time()
            self.check_events()
            self.render()
            self.clock.tick(60)