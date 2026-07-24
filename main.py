import os
import gradio as gr
import numpy as np

def predict_battery_soh(voltage, temperature, charge_cycles, current_draw):
    """
    Simulates AI prediction for Battery State of Health (SoH %) and Thermal Risk.
    """
    voltage_factor = (voltage - 300) / (420 - 300)
    cycle_degradation = (charge_cycles / 1500) * 15
    temp_penalty = max(0, (temperature - 35) * 0.4)
    current_penalty = (current_draw / 200) * 2
    
    estimated_soh = 100 - cycle_degradation - temp_penalty - current_penalty
    estimated_soh = max(10.0, min(100.0, estimated_soh))
    
    thermal_alert = "⚠️ HIGH THERMAL RISK DETECTED" if temperature > 45.0 else "✅ NOMINAL TEMPERATURE"
    system_status = "HEALTHY" if estimated_soh > 80 else "NEEDS INSPECTION"
    
    report = f"""
    ### 📊 AI Battery Diagnostic Summary
    * **State of Health (SoH):** {estimated_soh:.2f}%
    * **Thermal Status:** {thermal_alert}
    * **System Recommendation:** {system_status}
    """
    return report

with gr.Blocks(theme=gr.themes.Soft(), title="AI Battery BMS Diagnostics") as demo:
    gr.Markdown(
        """
        # ⚡ Predictive AI Battery Diagnostics (SoH Engine)
        ### Real-time Battery Health & Thermal Risk Inference Demo
        Adjust the telemetry sliders below to evaluate the Machine Learning model's response in real-time.
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎛️ Live Telemetry Inputs")
            voltage = gr.Slider(minimum=300.0, maximum=420.0, value=398.0, step=0.5, label="Pack Voltage (V)")
            temperature = gr.Slider(minimum=-10.0, maximum=60.0, value=28.0, step=0.5, label="Cell Temperature (°C)")
            charge_cycles = gr.Slider(minimum=0, maximum=1500, value=250, step=10, label="Charge Cycles Completed")
            current_draw = gr.Slider(minimum=0.0, maximum=200.0, value=25.0, step=1.0, label="Current Draw / Load (A)")
            btn = gr.Button("⚡ Run AI Diagnostic", variant="primary")
            
        with gr.Column():
            gr.Markdown("### 📈 Diagnostic Output")
            output = gr.Markdown(label="Diagnostic Report")
            
    btn.click(
        fn=predict_battery_soh,
        inputs=[voltage, temperature, charge_cycles, current_draw],
        outputs=output
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
