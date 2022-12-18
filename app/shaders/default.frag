#version 330 core
#extension GL_ARB_separate_shader_objects : enable

layout (location = 0) out vec4 fragColor;

void main() {
    vec3 color = vec3(1, 0, 0);
    fragColor = vec4(color, 1.0);
}