# Problem guides. Blocks: str = paragraph, list = bullet list, ("ol", [...]) = numbered list.
# Links: [[path|text]]
GUIDES = [
dict(
 slug="mechanical-seal-keeps-failing",
 h1="Why does my mechanical seal keep failing?",
 title="Why Mechanical Seals Keep Failing: Causes and Fixes",
 meta="A pump seal that fails again and again is reacting to dry running, a failed flush, shaft movement or the wrong materials. How to read the seal and fix it.",
 query="why does my mechanical seal keep failing",
 nav="Mechanical seal keeps failing",
 short="A mechanical seal that fails repeatedly is almost always reacting to something else in the pump or the system: dry running, a flush that is not reaching the faces, shaft movement from running away from the pump's best efficiency point, or materials that do not suit the fluid. Replacing the seal treats the symptom. Reading the failed seal faces tells you which cause to fix.",
 table=("What the failed seal is telling you", ["What you see", "Likely cause", "Check"], [
  ["Fine radial cracks on a hard face (heat checking)", "Faces ran dry, or the liquid flashed to vapor between them", "Flush flow and pressure, venting at start-up, suction conditions"],
  ["Chipped edges on the carbon face", "Vibration, or vapor forming and collapsing at the faces", "Cavitation, where the pump runs on its curve, the flush plan"],
  ["Wear track wider than the narrow face", "Shaft runout, misalignment or shaft deflection", "Alignment, bearing condition, distance from best efficiency point"],
  ["Deep grooves across the faces", "Abrasive solids between the faces", "Flush source cleanliness, face materials"],
  ["Swollen, soft or sticky O-rings", "Chemical attack on the elastomer", "Elastomer compatibility with the fluid and any cleaning chemicals"],
  ["Hard, cracked or flattened O-rings", "Too much heat", "Flush cooling, face heat, the elastomer's temperature limit"],
  ["Leaks from the first day", "Installation: wrong setting length, nicked O-ring, dirty faces", "Installation procedure, or move to a cartridge seal"],
 ]),
 sections=[
  ("Dry running and lost flush", [
   "Seal faces ride on a film of liquid a few microns thick. Lose that film for even a short time and the faces overheat. It happens when a pump is started before it is primed and vented, when the flush line or its orifice is blocked, or when the suction tank runs empty.",
   ["Vent the seal chamber before every start.", "Confirm flush flow at the seal, not only at the source.", "Fit a [[manufacturers/load-controls/|power monitor]] that trips the motor on low load, the signature of a dry pump.", "On water-flushed seals, use [[manufacturers/safematic/|seal water control]] so flow is set and visible."],
  ]),
  ("Running away from best efficiency point", [
   "A centrifugal pump run well to the left or right of its best efficiency point puts an uneven load on the impeller. The shaft bends slightly on every revolution, the seal faces open and close, and they wear or chip. If the pump also eats bearings, this is the first place to look. See [[problems/pump-running-off-curve/|how to tell if a pump is running off its curve]].",
  ]),
  ("Wrong materials for the fluid", [
   "Face pairs and elastomers have to suit the liquid, its temperature and any solids. A carbon face that works in clean water will not last in a slurry, and an elastomer that suits one chemical can swell or dissolve in another. Process changes, new cleaning chemicals and higher temperatures all catch out seals that were correctly chosen years ago.",
  ]),
  ("A flush plan that no longer fits", [
   "The flush plan controls the environment at the faces. Recirculating process liquid from the discharge works for clean, cool fluids. Liquids that are hot, dirty or close to their boiling point usually need a clean external flush or a dual seal with a barrier fluid. If the service has changed since the pump was installed, review the plan.",
  ]),
  ("Installation and mechanical condition", [
   "A seal cannot run true on a shaft that does not. Check shaft runout, end play and bearing condition before fitting a new seal; a commonly quoted limit for runout at the seal is about 0.002 in (0.05 mm). Component seals are set by hand and are easy to set wrong. Cartridge seals arrive preset and remove that risk.",
  ]),
  ("How to stop the repeat", [
   ("ol", ["Keep the failed seal. Do not clean it.", "Photograph both faces and the O-rings.", "Record run hours since the last change, and the flow, pressures and temperature the pump was running at.", "Have the seal examined and the cause written down, not just the part replaced.", "Track failures per pump so the next one is compared with the last."]),
   "Southern Design does this as [[services/mechanical-seal-repair/|seal repair with root cause failure analysis]], and tracks the history for contract customers in the [[services/reliability-management/|Reliability Management System]].",
  ]),
 ],
 faq=[
  ("How long should a mechanical seal last?", "There is no single figure. In a clean, cool, steady service a seal commonly runs for several years. If the same pump needs a seal more than once a year, the cause is in the pump or the system, not the seal."),
  ("Is some leakage from a mechanical seal normal?", "A working seal passes a very small amount of vapor that you normally cannot see. A visible, steady drip means the faces are damaged or not closing."),
  ("Will a cartridge seal fix repeat failures?", "It removes installation and setting errors. It will not fix dry running, a failed flush or a pump operating off its curve."),
  ("Can a failed mechanical seal be repaired?", "Often, yes. Faces can be relapped or replaced and elastomers renewed, and an exchange program keeps a ready seal on the shelf while the failed one is rebuilt."),
 ],
 services=["mechanical-seal-repair", "pump-repair", "reliability-management"],
 brands=["john-crane", "ppc", "us-seal", "flex-a-seal", "safematic", "load-controls"],
),
dict(
 slug="pump-cavitation",
 h1="Pump cavitation: signs, causes and how to stop it",
 title="Pump Cavitation: Signs, Causes and How to Stop It",
 meta="Cavitation sounds like gravel in the pump and destroys impellers, seals and bearings. The signs, the causes on the suction side, and the fixes that work.",
 query="pump cavitation causes and fixes",
 nav="Pump cavitation",
 short="Cavitation happens when pressure at the pump inlet falls below the liquid's vapor pressure. Vapor bubbles form, then collapse violently inside the impeller. It sounds like gravel passing through the pump, it erodes the impeller, and the vibration shortens seal and bearing life. The fix is on the suction side: raise the net positive suction head available (NPSHa) or reduce what the pump requires (NPSHr).",
 table=("Signs and what they point to", ["What you notice", "Likely cause", "Check"], [
  ["Crackling or gravel noise that gets worse as flow rises", "Suction cavitation", "NPSHa against NPSHr at that flow"],
  ["Noise at low flow that eases as the discharge valve opens", "Recirculation inside the impeller", "How far left of best efficiency point the pump runs"],
  ["Pitting on the impeller vanes near the inlet", "Cavitation over a long period", "Suction conditions since the last overhaul"],
  ["Discharge pressure and flow that will not hold steady", "Vapor or entrained air", "Tank level, vortexing, air leaks in the suction line"],
  ["Seals and bearings failing early on the same pump", "Vibration from any of the above", "All of the above before replacing parts"],
 ]),
 sections=[
  ("What causes it", [
   ["Suction tank level too low, or the pump lifting from too far below.", "A clogged suction strainer or a partly closed suction valve.", "Suction pipe that is too long, too small or has too many fittings.", "Liquid that is hotter than the design assumed. Vapor pressure rises with temperature.", "Running too far right on the curve. NPSHr climbs as flow rises.", "A speed increase without rechecking suction conditions."],
  ]),
  ("NPSH in one paragraph", [
   "NPSHa is the pressure pushing liquid into the pump, expressed as head: the absolute pressure on the liquid surface, plus the height of the liquid above the pump centerline (minus if the pump lifts), minus friction losses in the suction line, minus the liquid's vapor pressure. It has to exceed the NPSHr on the pump curve with margin. The NPSHr printed on most curves is the point where the pump has already lost 3% of its head, so a pump running exactly at NPSHr is already cavitating.",
  ]),
  ("How to fix it", [
   ["Raise the liquid level or lower the pump.", "Clean the suction strainer and open suction valves fully.", "Never throttle the suction valve to control flow. Control on the discharge.", "Shorten or enlarge the suction pipe, and give the pump a straight run into the inlet.", "Cool the liquid if the process allows.", "Move the operating point left by throttling the discharge or slowing the pump with a variable frequency drive.", "If the system cannot change, select a pump with a lower NPSHr."],
   "When the right fix is not obvious, [[services/hydraulic-system-analysis/|a hydraulic simulation of the system]] shows which change buys the most margin before anything is cut or bought.",
  ]),
  ("Cavitation or air?", [
   "Entrained air makes a similar noise and the same unstable gauge readings. Air gets in through a vortex in a shallow tank, through packing or flange joints on a suction line under vacuum, or from a return line that discharges above the liquid surface. Air problems do not usually pit the impeller, and they often change when the tank level changes.",
  ]),
 ],
 faq=[
  ("How quickly does cavitation damage a pump?", "Severe cavitation can pit an impeller within weeks. Mild cavitation may run for years while steadily shortening seal and bearing life. Either way the damage accumulates."),
  ("Does a variable frequency drive fix cavitation?", "Slowing the pump reduces both flow and NPSHr, which often stops it. Speeding the pump up makes cavitation worse."),
  ("How much NPSH margin do I need?", "There is no universal number. It depends on the pump type and how critical the service is. Common rules of thumb are a few feet above NPSHr, or a ratio of NPSHa to NPSHr comfortably above 1.1, with more margin for high-energy pumps. The Hydraulic Institute publishes guidance."),
 ],
 services=["hydraulic-system-analysis", "field-service", "pump-repair"],
 brands=["flexicraft", "load-controls", "mri"],
),
dict(
 slug="pump-running-off-curve",
 h1="Is your pump running off its curve? How to tell and what to do",
 title="Pump Running Off Its Curve: How to Tell and What to Do",
 meta="A pump run far from its best efficiency point bends its shaft and wears out seals and bearings. How to find the operating point and bring it back.",
 query="pump operating away from best efficiency point",
 nav="Pump running off its curve",
 short="A centrifugal pump is designed to run near its best efficiency point (BEP). Run it well to the left or right of that point and the hydraulic forces on the impeller rise sharply, bending the shaft and overloading the seal and bearings. If the same pump keeps needing seals or bearings, find out where it actually operates before replacing parts again.",
 table=("Left or right of best efficiency point", ["Where it runs", "What you notice", "Usual reasons"], [
  ["Left of BEP (too little flow)", "High discharge pressure, low motor amps, heat, vibration, noise that eases when the discharge valve opens", "Oversized pump, throttled discharge valve, demand lower than design"],
  ["Right of BEP (too much flow)", "Low discharge pressure, high amps or motor trips, cavitation noise", "System resistance lower than design, bypass left open, a parallel pump switched off"],
 ]),
 sections=[
  ("How to find the operating point", [
   ("ol", ["Read suction and discharge pressure at the pump.", "Convert the difference to head: feet of head = psi x 2.31 / specific gravity.", "Read flow if there is a meter, and motor amps.", "Plot the point on the manufacturer's curve for the impeller diameter and speed actually installed."]),
   "If the point sits well away from BEP, or does not sit on the curve at all, you have found something worth fixing. A point below the curve means internal wear or a wrong impeller.",
  ]),
  ("How far off is too far", [
   "The Hydraulic Institute describes a preferred operating region, commonly quoted as roughly 70% to 120% of BEP flow for most centrifugal pumps. Inside it, life is governed by normal wear. Outside it, shaft deflection, recirculation and cavitation shorten the life of seals and bearings.",
  ]),
  ("Why it happens", [
   "Safety factors get stacked at the design stage, so the pump arrives oversized. Processes change and nobody revisits the pump. Or a control valve is left to absorb the difference, burning energy and pushing the pump left.",
  ]),
  ("Ways to fix it", [
   ["Trim the impeller to suit the real duty.", "Fit a variable frequency drive and slow the pump down.", "Replace the pump or the impeller with one sized for the actual flow and head.", "Add a minimum-flow bypass for pumps that must run at low demand.", "Remove the restriction in the system if the pump is being held back."],
   "Southern Design models the system with [[services/hydraulic-system-analysis/|computer hydraulic simulation]] to choose between these before money is spent, and supplies [[manufacturers/toshiba/|Toshiba drives]] where slowing the pump is the answer.",
  ]),
  ("Protect the pump in the meantime", [
   "A [[manufacturers/load-controls/|power monitor]] reads motor load and trips the pump when it drifts too far in either direction. It is inexpensive protection while the permanent fix is planned.",
  ]),
 ],
 faq=[
  ("What is best efficiency point?", "It is the flow at which the pump converts the most shaft power into hydraulic power. It is also where the forces on the impeller are most balanced, which is why reliability is best there."),
  ("Can I leave the discharge valve throttled permanently?", "It works hydraulically, but it wastes energy at the valve, and if it pushes the pump too far left it trades one problem for another. Treat it as a temporary measure."),
  ("How do I convert pressure to head?", "Feet of head equals pressure in psi multiplied by 2.31 and divided by the liquid's specific gravity. For water, 10 psi is about 23 feet."),
 ],
 services=["hydraulic-system-analysis", "reliability-management", "field-service"],
 brands=["load-controls", "toshiba", "mri"],
),
dict(
 slug="pump-bearing-failure",
 h1="Why pump bearings fail early, and how to make them last",
 title="Why Pump Bearings Fail Early and How to Stop It",
 meta="Pump bearings rarely wear out. They fail from contaminated or wrong lubricant and from loads they were not chosen for. What the bearing and the oil tell you.",
 query="pump bearing failure causes",
 nav="Pump bearings failing early",
 short="Pump bearings rarely wear out from age. They fail early because the lubricant is contaminated, the wrong type or the wrong amount, or because the bearing is carrying loads it was not selected for: misalignment, imbalance, or hydraulic forces from running off the pump curve. Keep the oil clean, dry and at the right level, correct the loads, and most early bearing failures stop.",
 table=("What the bearing and the oil are telling you", ["What you see", "Likely cause", "Check"], [
  ["Milky or cloudy oil", "Water in the housing", "Housing seals or isolators, breather, wash-down practice"],
  ["Dark oil with a burnt smell", "Overheating: overfilled, wrong viscosity or overload", "Oil level, oil grade, bearing load"],
  ["Flaking on one side of the raceway", "Misalignment or excess thrust", "Shaft alignment, where the pump runs on its curve"],
  ["Evenly spaced lines across the raceway (fluting)", "Electrical current passing through the bearing, often with a variable frequency drive", "Shaft grounding, insulated bearings"],
  ["Rust-colored marks on the bore or outside diameter", "A loose fit on the shaft or in the housing", "Shaft and housing dimensions"],
  ["Dents at ball or roller spacing", "Damage during installation", "How bearings are fitted and handled"],
 ]),
 sections=[
  ("Contamination", [
   "Water and dirt are the usual killers. Lip seals wear a groove in the shaft and then let in wash-down water and dust. Housings breathe moist air every time they cool.",
   ["Replace lip seals with [[manufacturers/isomag/|bearing isolators]].", "Fit desiccant breathers.", "Store and transfer oil in sealed, labeled containers."],
  ]),
  ("Oil level and quantity", [
   "Too little oil starves the bearing. Too much churns and overheats it. On most oil-bath pump housings the correct level is around the center of the lowest ball. Constant level oilers hold that level only if they are set correctly, and a sight glass lets anyone confirm it at a glance. With grease, over-packing causes as many failures as neglect. [[manufacturers/trico/|Trico]] supplies the oilers, sight glasses and breathers.",
  ]),
  ("The wrong lubricant", [
   "Viscosity has to suit the bearing's speed and running temperature. Topping up with a different oil, or mixing incompatible greases, can leave a bearing worse off than it was.",
  ]),
  ("Loads the bearing was not selected for", [
   ["Misalignment between pump and motor, including pipe strain and soft foot.", "Radial load from [[problems/pump-running-off-curve/|running away from best efficiency point]].", "Imbalance after an impeller trim or repair.", "Vibration from [[problems/pump-cavitation/|cavitation]]."],
  ]),
  ("Turn it into a program", [
   "One-off fixes fade. A lubrication program holds the gains: the right lubricant at every point, clean storage, set routes and people trained to carry them out. Southern Design runs [[services/lubrication-training-audits/|plant lubrication audits and ICML certification training]] and supplies [[manufacturers/lube-it/|Lube-It]] software to manage the routes.",
  ]),
 ],
 faq=[
  ("How often should pump bearing oil be changed?", "Follow the pump manufacturer's interval as a starting point, then adjust for temperature and contamination. Oil analysis is a better guide than the calendar."),
  ("How hot is too hot for a pump bearing housing?", "Many housings run warm to the touch as a matter of course. A steady reading matters less than a change: a housing that suddenly runs hotter than it used to needs attention. Check the manufacturer's limit for the pump."),
  ("Do bearing isolators replace lip seals?", "Yes. They fit in the same housing bore, do not wear the shaft, and keep out water and dust far more effectively."),
 ],
 services=["lubrication-training-audits", "pump-repair", "reliability-management"],
 brands=["isomag", "trico", "lube-it", "amrri", "basetek"],
),
dict(
 slug="calculate-pump-mtbf",
 h1="How to calculate pump MTBF and find your bad actors",
 title="How to Calculate Pump MTBF and Find Bad Actors",
 meta="Pump MTBF is pumps in service times months, divided by failures. A worked example, what counts as a failure, and how to find the few pumps eating the budget.",
 query="how to calculate pump MTBF",
 nav="Calculating pump MTBF",
 short="Pump MTBF (mean time between failures) is the number of pumps in service multiplied by the time period, divided by the number of failures in that period. A plant with 400 pumps and 160 failures in 12 months has an MTBF of 30 months. The plant-wide number shows the trend. The per-pump numbers show which few machines, the bad actors, are consuming most of the repair budget.",
 table=("Worked example", ["Input", "Value"], [
  ["Pumps in service", "400"],
  ["Period", "12 months"],
  ["Failures in the period", "160"],
  ["MTBF = (400 x 12) / 160", "30 months"],
 ]),
 sections=[
  ("Decide what counts as a failure", [
   "The number only means something if a failure is defined the same way every time. A workable definition: any unplanned event that needs the pump opened or removed, including a seal change. Planned preventive work does not count. Write the definition down and keep to it.",
  ]),
  ("Calculate it per pump as well as for the plant", [
   "The plant-wide figure hides the detail. One pump that has failed five times in 18 months and one that has run for six years both disappear into the same average. Per-pump history is where the decisions are.",
  ]),
  ("Find the bad actors", [
   ("ol", ["List every pump with its failures over the last two to three years.", "Add the cost of each failure: repair parts, labor and downtime.", "Rank by total cost, then by number of failures.", "The same few tags will sit at the top of both lists. Those are the bad actors."]),
   "In most plants a small share of the pumps accounts for a large share of the failures and the spend. That is good news: fixing a handful of machines moves the plant-wide number.",
  ]),
  ("What to do with the list", [
   "Each bad actor gets a root cause analysis, not another repair. The causes repeat: [[problems/pump-running-off-curve/|running off the curve]], [[problems/mechanical-seal-keeps-failing/|seal environment]], [[problems/pump-bearing-failure/|lubrication]], [[problems/pump-cavitation/|suction conditions]]. Fix the cause, then watch the pump's own MTBF to confirm it worked.",
  ]),
  ("The data you need", [
   ["A complete, accurate equipment list.", "Every repair with its date, what was found and what was replaced.", "Parts and labor cost per repair.", "An estimate of downtime cost per pump."],
   "Most plants have this spread across work orders, purchase orders and people's memories. Southern Design's [[services/reliability-management/|Reliability Management System]] builds the database, reports MTBF and cost per machine, and tracks each root cause from failure to fix.",
  ]),
 ],
 faq=[
  ("What is a good MTBF for pumps?", "It varies widely with the industry, the type of pump and how failure is defined, so comparisons between plants are unreliable. The useful comparison is your own number against last year's."),
  ("How much history do I need?", "At least 12 months to get a number, and two to three years to identify bad actors with confidence."),
  ("What is the difference between MTBF and MTTR?", "MTBF measures how often equipment fails. MTTR, mean time to repair, measures how long it takes to get it running again. Reliability work raises the first; maintenance planning lowers the second."),
 ],
 services=["reliability-management", "pump-repair"],
 brands=["mri"],
),
dict(
 slug="water-hammer-pulsation",
 h1="Water hammer and pulsation in pump systems: causes and fixes",
 title="Water Hammer and Pulsation in Pump Systems: Fixes",
 meta="Banging pipes, swinging gauges and broken supports come from water hammer or pump pulsation. What causes each and how dampeners, valves and drives fix them.",
 query="water hammer in pump system fix",
 nav="Water hammer and pulsation",
 short="Water hammer is a pressure surge caused by liquid being stopped or started suddenly, usually by a fast-closing valve or a pump tripping. Pulsation is the rhythmic pressure swing that diaphragm, piston and other positive displacement pumps produce on every stroke. Both shake piping, break supports and damage gauges and seals. Both are fixed by slowing the change in velocity or absorbing it with a surge suppressor or pulsation dampener.",
 table=("Which one do you have?", ["What you notice", "Likely cause", "Check"], [
  ["A bang when a valve closes", "Water hammer from fast closure", "Valve type and closing time"],
  ["A bang when the pump stops", "Check valve slam, or the liquid column separating and rejoining", "Check valve type, how the pump is stopped"],
  ["A rhythmic thump in time with a diaphragm or piston pump", "Pulsation", "Whether a dampener is fitted, and its charge pressure"],
  ["Gauge needles swinging, pipe moving at start-up", "Pulsation, or air pockets and a fast start", "Dampener, venting, how the pump is started"],
 ]),
 sections=[
  ("Why it hits so hard", [
   "Moving liquid has momentum. Stop it instantly in a steel pipe and the pressure rises by very roughly 50 psi for every 1 ft/s of velocity that was stopped. A line flowing at 8 ft/s can see a surge several times its working pressure.",
  ]),
  ("Fixing water hammer", [
   ["Slow the valve. Longer closing times and controlled actuator speed remove most surges. [[manufacturers/pmv/|Positioners]] give that control on automated valves.", "Use non-slam check valves on pump discharges.", "Ramp pumps down with a [[manufacturers/toshiba/|variable frequency drive]] instead of tripping them.", "Use [[manufacturers/cla-val/|pump control and surge anticipating valves]] on long pipelines.", "Fit a [[manufacturers/blacoh/|surge suppressor]] close to the valve or pump that causes the surge."],
  ]),
  ("Fixing pulsation", [
   ["Fit a [[manufacturers/blacoh/|pulsation dampener]] on the discharge, as close to the pump as practical.", "Set the dampener charge to the manufacturer's recommendation for your system pressure. A dampener with the wrong charge does very little.", "On the suction side, an inlet stabilizer keeps the pump fed and stops the suction line shaking.", "Use [[manufacturers/flexicraft/|flexible connectors]] to keep vibration out of rigid pipework."],
  ]),
  ("When to model it", [
   "On long lines, high velocities or systems with several pumps and valves, surge behavior is hard to judge by eye. [[services/hydraulic-system-analysis/|Hydraulic simulation]] shows where the pressure peaks will be and what size of suppressor or change in valve timing removes them.",
  ]),
 ],
 faq=[
  ("Is water hammer dangerous?", "It can be. Repeated surges loosen supports and fatigue joints, and a severe surge can exceed the pressure rating of pipe, valves and instruments."),
  ("Where should a pulsation dampener be installed?", "On the pump discharge, as close to the pump as practical, with as few bends as possible between the two."),
  ("Do I need a dampener on the suction side too?", "If the suction line is long or the pump is starving on each stroke, an inlet stabilizer helps the pump fill and protects the suction piping."),
 ],
 services=["hydraulic-system-analysis", "field-service"],
 brands=["blacoh", "cla-val", "flexicraft", "graco", "pmv"],
),
dict(
 slug="mag-drive-pump-failure",
 h1="Why mag-drive pumps fail: dry running, decoupling and solids",
 title="Why Mag-Drive Pumps Fail: Dry Running, Decoupling",
 meta="Magnetic drive pumps have no seal to leak, but they fail from dry running, low flow, decoupling and solids. How to recognize each and protect the pump.",
 query="why do mag drive pumps fail",
 nav="Mag-drive pump failures",
 short="Magnetic drive pumps have no shaft seal to leak, but they rely on the pumped liquid to cool and lubricate their internal bushings. Most mag-drive failures come from running dry, running at too little flow, decoupling the magnets under excess torque, or passing solids through close internal clearances. Most are preventable with a power monitor and correct sizing for the liquid's specific gravity and viscosity.",
 table=("What you find and what it means", ["What you find", "Likely cause", "Check"], [
  ["Pump turning, no flow, motor load low", "Magnets decoupled, or the pump is dry", "Suction supply, start-up conditions, liquid specific gravity and viscosity"],
  ["Melted or distorted plastic parts, cracked bushings", "Ran dry", "Tank level control, operator procedure, dry-run protection"],
  ["Scored shaft and bushings", "Solids in the liquid", "Suction strainer, what is actually in the liquid"],
  ["Rub marks inside the containment shell", "Worn bushings let the rotor touch the shell", "Bushing wear at the last overhaul, run hours"],
  ["Heat damage after running at low flow", "Liquid in the drive section overheated or flashed", "Minimum flow, discharge valve position"],
 ]),
 sections=[
  ("Dry running", [
   "The bushings and thrust surfaces need liquid from the first second of operation. An empty suction tank, a closed suction valve or a lost prime can ruin them quickly. This is the most common mag-drive failure and the easiest to prevent.",
  ]),
  ("Decoupling", [
   "The magnets can only transmit so much torque. Ask for more and the inner magnet stops following the outer one: the motor spins, the impeller does not. It happens when the liquid is heavier or more viscous than the pump was sized for, on cold starts with thick liquid, or when solids jam the impeller. Stop the pump and restart it; running decoupled generates heat and can weaken the magnets.",
  ]),
  ("Too little flow", [
   "A small flow of liquid circulates behind the impeller to cool the drive. At very low flow that liquid heats up and can flash to vapor, which then behaves like dry running. Observe the manufacturer's minimum flow.",
  ]),
  ("Solids", [
   "Internal clearances are small. Abrasive particles wear the bushings and shaft, and ferrous particles collect on the magnets. Strain the suction, or choose a design made to pass solids.",
  ]),
  ("Protecting the pump", [
   ["Fit a [[manufacturers/load-controls/|power monitor]]. It reads motor power, which drops sharply when the pump runs dry or decouples, and trips the motor.", "Size the magnets for the real specific gravity and viscosity, including cold starts.", "Match the lining to the chemical: [[manufacturers/finish-thompson/|ETFE-lined]] and [[manufacturers/richter/|PFA-lined]] pumps cover most corrosive service, and [[manufacturers/liquiflo/|gear pumps]] cover metering duties."],
   "When one does fail, Southern Design carries out [[services/pump-repair/|mag-drive pump repair]] with a written cause.",
  ]),
 ],
 faq=[
  ("Can a mag-drive pump run dry at all?", "Some designs tolerate a brief dry start better than others, depending on bushing material. None should be run dry as a matter of practice. Protect the pump rather than rely on tolerance."),
  ("How do I know the magnets have decoupled?", "The motor runs but flow and pressure drop to nothing, and motor load falls well below normal. Stop the pump, find the reason, and restart."),
  ("When should I choose a mag-drive pump over a sealed pump?", "When a leak is unacceptable: toxic, corrosive, expensive or regulated liquids. For dirty or solids-laden liquids a sealed pump with the right seal is often the better choice."),
 ],
 services=["pump-repair", "hydraulic-system-analysis"],
 brands=["finish-thompson", "richter", "liquiflo", "load-controls"],
),
dict(
 slug="repair-or-replace-pump",
 h1="Should you repair or replace an industrial pump?",
 title="Repair or Replace an Industrial Pump? How to Decide",
 meta="Repair a pump that suits its duty and has a fixable cause. Replace one that is wrong for the job or costs too much to keep. Five questions that decide it.",
 query="repair or replace industrial pump",
 nav="Repair or replace a pump",
 short="Repair when the pump suits its duty, parts are available and the failure has a cause you can fix. Replace when the pump is wrong for the job, when the repair cost approaches the price of a new unit, or when waiting for parts will keep you down longer than a replacement would. The pump's repair history decides it more than the single failure in front of you.",
 table=("Five questions that decide it", ["Question", "Points to repair", "Points to replace"], [
  ["Is it the right pump for the duty?", "It runs near its best efficiency point and the materials suit the liquid", "It runs off its curve or the materials are being attacked"],
  ["What does its history say?", "Long runs between failures", "A bad actor with several failures in two to three years"],
  ["What will the repair cost?", "Well under half the price of a new pump", "Approaching or above half. Price both"],
  ["How long are parts?", "On the shelf or days away", "Long lead time or obsolete"],
  ["Can the repair include an upgrade?", "Yes: seal, bearing protection, baseplate, materials", "No upgrade would change the outcome"],
 ]),
 sections=[
  ("Start with the duty, not the damage", [
   "A pump that is wrong for its service will fail again however well it is rebuilt. Check [[problems/pump-running-off-curve/|where it runs on its curve]] and whether the wetted materials suit the liquid before deciding anything.",
  ]),
  ("Look at the history", [
   "One failure after years of service is a repair. The fifth failure in 18 months is a pattern, and the money spent so far belongs in the comparison. If you do not have the history to hand, that is the first thing to fix; see [[problems/calculate-pump-mtbf/|how to calculate MTBF and find bad actors]].",
  ]),
  ("Cost and lead time", [
   "A common rule of thumb is to price a replacement once a repair passes about half the cost of a new pump. Add the cost of downtime while parts arrive. For common ANSI process pumps, [[manufacturers/hisco/|Hisco]] supplies complete pumps and parts to fit Goulds, Flowserve and Summit models, which often shortens the wait.",
  ]),
  ("Upgrade while it is apart", [
   ["Change a component seal for a cartridge seal.", "Replace lip seals with bearing isolators.", "Move to a [[manufacturers/basetek/|corrosion-resistant baseplate]] if the old one has gone.", "Correct the impeller diameter if the pump has been running off its curve."],
  ]),
  ("What a good repair includes", [
   "A written inspection with measurements and photographs, the cause of failure, fits and clearances restored, the rotor balanced, and a record that goes into the pump's history. Southern Design's [[services/pump-repair/|pump repair]] is done this way.",
  ]),
 ],
 faq=[
  ("Is it worth repairing a pump that keeps failing?", "Only if the repair also removes the cause. Otherwise you are paying for the same failure again."),
  ("Can a pump be upgraded during a repair?", "Yes. Seals, bearing protection, materials and impeller diameter can all be changed while the pump is apart, usually for far less than a new unit."),
  ("Are aftermarket pump parts reliable?", "Parts made to the original dimensions and materials by an established manufacturer perform as the originals do. Ask what the part is made of and who made it."),
 ],
 services=["pump-repair", "mechanical-seal-repair", "reliability-management"],
 brands=["hisco", "basetek", "nomad"],
),
dict(
 slug="pump-reliability-program",
 h1="How to set up a pump reliability program",
 title="How to Set Up a Pump Reliability Program: 7 Steps",
 meta="A pump reliability program is a list of what you have, a record of every failure and its cost, and root cause work on the worst pumps. Seven steps to start.",
 query="pump reliability program",
 nav="Setting up a reliability program",
 short="A pump reliability program is a routine for finding out which pumps fail most, why, and what stops it. It needs three things: an accurate list of the pumps you have, a record of every failure with its cause and cost, and one person responsible for working through the worst machines. In most plants a small share of the pumps accounts for a large share of the repair spend, so the first job is to find them.",
 table=("What to record for every failure", ["Record", "Why it matters", "Where it usually comes from"], [
  ["Pump tag and service", "Ties the failure to one machine, not to a model", "Equipment list"],
  ["Date, and run time since the last repair", "Gives the time between failures", "Work order, hour meter"],
  ["What failed: seal, bearing, coupling, impeller, motor", "Shows the pattern on that pump", "Repair report"],
  ["Why it failed: the cause, not the part", "The only thing that prevents the next one", "Root cause analysis"],
  ["Parts and labor cost", "Ranks pumps by money, not by how often they are mentioned", "Purchase orders, time sheets"],
  ["Downtime, and what it cost", "Often larger than the repair itself", "Operations"],
 ]),
 sections=[
  ("1. List what you have", [
   "Walk the plant and record what is actually installed: tag, service, make, model, size, seal, motor. Records drift as pumps are swapped and rebuilt, so do not rely on the old list. Then rate each pump by what happens when it stops: a safety or environmental risk, lost production, or nothing because the spare takes over. That rating decides where the effort goes.",
  ]),
  ("2. Record every failure and what it cost", [
   "Agree what counts as a failure and keep to it. A common definition is any event that takes the pump out of service for repair. Record each one against the pump's tag, using the table above. Cost matters as much as count: a pump that fails twice a year at high cost deserves attention before one that fails four times for the price of a seal.",
  ]),
  ("3. Measure and rank", [
   "Calculate mean time between failures for the plant and for each pump; the guide to [[problems/calculate-pump-mtbf/|calculating pump MTBF]] has the formula and a worked example. Then sort the list by number of failures and by cost. The pumps at the top are the bad actors, and the list is usually short.",
  ]),
  ("4. Find the cause of each repeat failure", [
   "A bad actor gets a root cause analysis, not another repair. Keep the failed parts, read them, and check how the pump was running. The same causes come up from plant to plant:",
   ["The pump runs away from its best efficiency point. See [[problems/pump-running-off-curve/|running off the curve]].",
    "The seal runs dry, or its flush is not working. See [[problems/mechanical-seal-keeps-failing/|why seals keep failing]].",
    "Lubrication: the wrong oil, too much grease, or water and dirt getting in. See [[problems/pump-bearing-failure/|why bearings fail early]].",
    "Too little pressure at the pump inlet. See [[problems/pump-cavitation/|pump cavitation]].",
    "Misalignment, pipe strain or a baseplate that flexes."],
  ]),
  ("5. Fix the cause and write down the standard", [
   "Make the change the analysis points to: trim the impeller or change the control so the pump runs near its best efficiency point, correct the seal flush, fit bearing protection, regrout the base. Then make it the standard, so the next repair does not undo it: alignment tolerances, how seals are installed, which lubricant goes where. A repair shop that reports the cause with every repair makes this much easier.",
  ]),
  ("6. Watch condition between failures", [
   "Once the worst pumps are dealt with, monitoring catches the next problem early.",
   ["Vibration readings on a route, or continuous monitoring on critical machines",
    "Motor power monitoring, which shows dry running and off-design operation. See [[manufacturers/load-controls/|power monitors]].",
    "Oil analysis and a planned lubrication program. See [[services/lubrication-training-audits/|lubrication audits and training]].",
    "Operator rounds: leaks, noise, temperature, oil level"],
  ]),
  ("7. Review the numbers on a schedule", [
   "Look at MTBF, cost per pump and the bad actor list at a fixed interval, monthly or quarterly. Close out each root cause action and check that the pump has stopped failing. A program that is not reviewed turns back into a repair log.",
  ]),
  ("Who should run it", [
   "One named person, with time set aside for it. In a small plant that is the maintenance or reliability lead. Plants without that person can contract it: Southern Design's [[services/reliability-management/|Reliability Management System]] builds the equipment database, reports MTBF and cost per machine, and assigns a lead reliability engineer to work through the bad actors with you.",
  ]),
 ],
 faq=[
  ("What is a pump reliability program?", "A routine for recording pump failures, finding their causes and fixing those causes, so the same pumps stop failing. It combines an equipment list, failure and cost records, root cause analysis and condition monitoring."),
  ("What is a bad actor?", "A pump that fails far more often, or costs far more to keep running, than the rest. Bad actors are where a reliability program starts."),
  ("Do we need software to start?", "No. A spreadsheet with one row per failure is enough to start. Software earns its place when there are too many pumps and repairs for one person to keep straight."),
  ("How long before a reliability program shows results?", "The bad actor list is usually clear once a year of failure records is in one place. Results follow as each cause is fixed, so the timing depends on how quickly the changes are made."),
 ],
 services=["reliability-management", "pump-repair", "lubrication-training-audits"],
 brands=["load-controls", "mri", "trico", "isomag"],
),
]
