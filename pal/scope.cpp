#include "scope.h"
#include "imgui/imgui.h"

Scope::Scope(int l) :
    data(l, 0)
{

}

void Scope::write(float x)
{
    if (freeze)
    {
        return;
    }

    data[writeIndex] = x;
    writeIndex = (writeIndex + 1) % data.size();
}

void Scope::draw()
{
    ImGui::PlotLines("Scope", data.data(), data.size(), 0, "", -1, 1, ImVec2(0,80));

    /*
    ImGui::SliderFloat("trigger label", &trigger, -1, 1);
    ImGui::Checkbox("trigger enabled", &triggerEnabled);
    */
    ImGui::Checkbox("Freeze", &freeze);
}