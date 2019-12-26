#pragma once

#include <imgui.h>
#include <imgui_impl_sdl.h>
#include <imgui_impl_opengl2.h>
#include <stdio.h>
#include <SDL.h>
#include <SDL_opengl.h>
#include <functional>

class Gui
{
    public:
    virtual void layout() = 0;
    void show();

    protected:
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);
};

class QuickGui : public Gui
{
    public:
    QuickGui(std::function<void()> layoutFunction);
    void layout();

    private:
    std::function<void()> layoutFunction;
};

void quickGui(std::function<void()> layout);