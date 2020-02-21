#include "adsr.h"
#include "imgui/imgui.h"
#include <cmath>

Adsr::Adsr(float a, float d, float s, float r, float fs)
{
    attack = a;
    decay = d;
    sustain = s;
    rel = r;
    this->fs = fs;
}

void Adsr::draw()
{
    {
        ImGui::SliderFloat("Attack", &attack, 0.0, 10.0);
        ImGui::SliderFloat("Decay", &decay, 0, 10.0);
        ImGui::SliderFloat("Sustain", &sustain, 0, 1);
        ImGui::SliderFloat("Release", &rel, 0, 10);
    }

    if (isTriggered)
    {
        if (ImGui::Button("Untrigger"))
        {
            release();
        }
    }
    else
    {
        if (ImGui::Button("Trigger"))
        {
            trigger();
        }
    }
    
}

float Adsr::next()
{
    if (isTriggered)
    {
        if (timeSinceTrigger < attack)
        {
            value += (1.0 / fs) * (1.0 / attack);
        }
        else if (timeSinceTrigger < attack + decay)
        {
            value -= (1.0 / fs) * (1.0 / decay) * (1.0 - sustain);
        }

        timeSinceTrigger += (1.0 / fs);
    }
    else if (value > 0)
    {
        value -= sustain * (1.0 / fs) * (1.0 / rel);

        timeSinceRelease += (1.0 / fs);
    }
    else if (value < 0)
    {
        value = 0;
    }
    
    return value;
}

void Adsr::release()
{
    if (isTriggered)
    {
        isTriggered = false;
        timeSinceRelease = 0;
    }
}

void Adsr::trigger()
{
    if (!isTriggered)
    {
        isTriggered = true;
        timeSinceTrigger = 0;
    }
}