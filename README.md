# Packet Logger using SDN Controller (POX)

## 📌 Problem Statement

Capture and log packets traversing a network using SDN controller events. Identify protocols and enforce traffic policies.

---

## 🛠️ Tools Used

* Mininet
* POX Controller
* Python
* OpenFlow Protocol

---

## ⚙️ Features

* Packet capturing using controller events
* Protocol identification (ARP, ICMP, TCP, UDP)
* Logging to terminal and file
* Learning switch forwarding
* Firewall (blocking traffic from h3 → h1)

---

## 🌐 Network Topology

* 3 Hosts (h1, h2, h3)
* 1 Switch (s1)
* Remote SDN Controller (POX)

---

## 🚀 How to Run

### Step 1: Start Controller

```
cd pox
./pox.py openflow.of_01 --port=6633 misc.packet_logger
```

### Step 2: Start Topology

```
sudo python3 topology.py
```

---

## 🧪 Test Scenarios

### ✅ Normal Traffic

```
h1 ping h2
```

### ❌ Blocked Traffic

```
h3 ping h1
```

---

## 📊 Performance Testing

### Throughput

```
h1 iperf -s &
h2 iperf -c 10.0.0.1
```

### Flow Table

```
sudo ovs-ofctl dump-flows s1
```

---

## 📂 Output

* Logs displayed in controller terminal
* Logs saved in `packet_logs.txt`

---

## 📸 Screenshots

See `/screenshots` folder

---

## 🧠 Conclusion

This project demonstrates SDN-based packet monitoring and control using a centralized controller, enabling dynamic traffic management and network visibility.
