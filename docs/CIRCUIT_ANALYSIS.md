# Circuit Analysis — Omni-Harvester

## Mathematical Formulations

### 1. Diode-OR Combining Analysis
For $N$ energy harvesting modules connected to a shared DC bus via forward-biased Schottky diodes:

$$V_{bus} = \max_{k \in \{1..N\}} \left( V_{k,oc} - V_{D,k} \right)$$

where:
- $V_{k,oc}$ is the open-circuit output voltage of the $k$-th harvesting domain.
- $V_{D,k}$ is the forward conduction voltage drop of diode $D_k$ ($1\text{N}5819: V_D \approx 0.28\text{V} \text{ at } 10\text{mA}$).

The total instantaneous current $I_{bus}$ delivered to the storage element is:

$$I_{bus} = \sum_{k=1}^N I_k \cdot \mathcal{H}\left( V_{k} - V_{bus} - V_{D,k} \right)$$

where $\mathcal{H}(\cdot)$ is the Heaviside step function enforcing directional conduction.

---

### 2. Piezoelectric Rectification Stage
The mechanical excitation of the $35\text{mm}$ PZT piezoelectric disc produces an alternating voltage:

$$v_{pz}(t) = V_p \sin(\omega t)$$

Passing through the bridge rectifier (DF02M), the DC rectified voltage is:

$$V_{pz,dc} \approx V_p - 2 V_{f,bridge}$$

For an array of $M$ mechanically synchronized discs connected in parallel:

$$I_{pz,total} = M \cdot \left( \frac{V_{pz,dc}}{R_{int,pz}} \right)$$

---

### 3. Thermoelectric Generation (Seebeck Effect)
The voltage generated across the TEC1-12706 module is governed by the Seebeck coefficient $\alpha$:

$$V_{teg} = N \cdot \alpha \cdot \Delta T$$

where:
- $N$ is the number of thermocouple p-n pairs ($\approx 127$).
- $\alpha \approx 200\ \mu\text{V/K}$ per couple.
- $\Delta T = T_{hot} - T_{cold}$ is the thermal gradient.

The maximum power extracted under matched impedance conditions ($R_L = R_{int}$):

$$P_{teg,max} = \frac{V_{teg}^2}{4 R_{int}}$$

---

### 4. RF Harvester (Villard Multiplier)
The open-circuit DC voltage produced by an $N$-stage Villard charge pump ladder receiving ambient RF power $P_{rf}$:

$$V_{rf,out} = 2 N \left( \sqrt{2 R_{ant} P_{rf} \cdot 10^{\frac{G}{10}}} - V_{th,rf} \right)$$

Zero-bias germanium diodes (1N34A) provide an ultra-low threshold $V_{th,rf} \approx 0.15\text{V}$, enabling harvesting from sub-milliwatt incident fields.

---

### 5. Supercapacitor State-of-Charge Dynamics
The energy $E$ stored within the $1.0\text{ F}$ capacitor as a function of time:

$$E(t) = \frac{1}{2} C V_{cap}(t)^2$$

Differentiating with respect to time yields the net charging equation:

$$\frac{d E}{d t} = P_{in}(t) - P_{leak}(t) - \frac{P_{load}(t)}{\eta_{boost}}$$

$$C V_{cap}(t) \frac{d V_{cap}(t)}{d t} = I_{bus}(t) V_{bus}(t) - \frac{V_{cap}(t)^2}{R_{leak}} - \frac{V_{out} I_{load}(t)}{\eta_{boost}}$$

Integrating over a charging interval $\Delta t$:

$$V_{cap}(t + \Delta t) = \sqrt{ V_{cap}(t)^2 + \frac{2}{C} \int_{t}^{t+\Delta t} \left( P_{in}(\tau) - P_{loss}(\tau) \right) d\tau }$$
