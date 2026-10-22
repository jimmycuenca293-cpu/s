# -*- coding: utf-8 -*-
"""Guías (blog) de la tienda de EE. UU., en inglés. Cada guía: slug, title, desc, h1, intro, secciones, faq, brand (opcional), steps (opcional, para HowTo)."""
from catalog import BRANDS

G = []


def g(slug, title, desc, h1, intro, sections, faq, brand=None, steps=None, related=()):
    G.append(dict(slug=slug, title=title, desc=desc, h1=h1, intro=intro, sections=sections, faq=faq, brand=brand, steps=steps, related=list(related)))


g("how-often-to-change-a-refrigerator-water-filter",
  "How Often to Change a Refrigerator Water Filter (Every 6 Months?)",
  "Most refrigerator water filters should be replaced about every 6 months. Learn the signs it is time, what shortens filter life and how to track it.",
  "How often should you change a refrigerator water filter?",
  "Most refrigerator manufacturers recommend replacing the water filter about every six months. That is a guideline, not a law of nature: the right moment depends on how much water your household uses and how clean your water is to begin with.",
  [("The 6-month rule and why it exists", ["A refrigerator water filter works by trapping particles and reducing chlorine taste and odor with activated carbon. Carbon has a limited capacity. After roughly six months of normal use the cartridge is saturated, and it can no longer do its job well even though water still flows through it.",
                                           "Many refrigerators track this for you with a filter indicator light. The light is usually a timer or a gallon counter, so it is a reminder, not a measurement of your actual water quality."]),
   ("Signs it is time to change it sooner", ["Water or ice starts to taste or smell different.", "The dispenser fills a glass more slowly than it used to.", "Ice looks cloudy or the ice maker makes smaller cubes.", "The filter indicator light is on or flashing.", "You see sediment or particles in a glass of water."]),
   ("What shortens filter life", ["Heavy use (a large family or frequent entertaining), water with a lot of sediment, very hard water or well water can clog a filter well before six months.", "If you are away for a long period, the filter still ages, so check the date on the cartridge when you return."]),
   ("Keep track so you never forget", ["Write the install date on the filter with a marker, or set a reminder on your phone for six months out. When the reminder fires, find your part number in our filter finder and order the replacement a couple of weeks early."])],
  [("Can I change my refrigerator water filter after 12 months?", "It will still pass water, but a carbon filter that old is likely saturated and can no longer reduce chlorine taste or odor as intended. Most manufacturers recommend replacing it about every six months."),
   ("Does an unused filter expire?", "Keep a spare in its sealed packaging in a cool, dry place. Check the packaging for storage notes from the filter's manufacturer."),
   ("Do I have to replace the filter if the light is not on?", "No, but the light is only a timer or gallon estimate. If water tastes or flows differently, change the filter regardless of the light.")],
  related=["how-to-find-your-refrigerator-model-number", "how-to-change-a-refrigerator-water-filter"])

g("how-to-find-your-refrigerator-model-number",
  "How to Find Your Refrigerator Model Number (Where the Sticker Is)",
  "Need the right water filter? Find your refrigerator model number on the label inside the fridge, on the door frame or in the manual. Here is where to look.",
  "How to find your refrigerator model number",
  "The model number is the fastest way to find the correct water filter. It is printed on a label inside the refrigerator, and once you have it you can match it to a filter part number in seconds.",
  [("Where to look", ["Inside the fresh-food compartment on the upper side wall or the ceiling of the refrigerator.", "On the side wall below the crisper drawers or behind them. Pull the drawer out if the label is not visible.", "On the door frame or along the inside edge of the door opening, especially on French door models.", "On the back of the refrigerator or inside the freezer door of some models.", "In the owner's manual or on the original receipt and product page."]),
   ("What the number looks like", ["Model numbers are a mix of letters and digits. Samsung models often start with RF or RS (for example RF28HMEDBSR). LG models often start with LF, LM, LR or LS (for example LFX28968ST). Whirlpool-family models often start with W, K or M followed by letters (for example WRF555SDFZ). Copy the whole string exactly, including letters at the end."]),
   ("Do not confuse model number with serial number", ["The label lists both. The model number identifies the product line; the serial number identifies your individual unit. Use the model number to look up a water filter."]),
   ("If you cannot find it", ["Take a photo of the old filter and of any label you can find and send it to us on WhatsApp. We will help match it to the right filter before you order."])],
  [("Is the filter model the same as the refrigerator model?", "No. The refrigerator has a model number and the filter has its own part number (for example DA29-00020B or LT700P). One filter part number fits many refrigerator models."),
   ("Can I find my filter by the old filter's number?", "Yes. Many filters have a part number printed on the end or on the label. Search that number in our finder."),
   ("What if my model is not in your list?", "Message us with the model number or a photo of the old filter. We will tell you which filter fits or if we do not carry it yet.")],
  related=["how-to-tell-which-refrigerator-water-filter-fits"])

g("how-to-change-a-refrigerator-water-filter",
  "How to Change a Refrigerator Water Filter: Step-by-Step Guide",
  "Step-by-step instructions to replace an internal refrigerator water filter in a few minutes, without a plumber, and how to flush the new one.",
  "How to change a refrigerator water filter (step by step)",
  "Replacing a refrigerator water filter takes about five minutes and needs no tools. The exact motion depends on the model, but the steps below apply to most internal filters.",
  [("Before you start", ["Have the new filter and a towel ready. Take the protective cap off the new filter only when you are about to install it.", "Check your owner's manual for the filter location. It is usually inside the fresh-food compartment (upper corner or back wall) or in the base grille at the bottom front."]),
   ("Steps", ["Locate the old filter and, if there is a cover, open it.", "Turn the filter counterclockwise (or push and release the button, depending on the model) and pull it straight out. A little water may drip: have the towel ready.", "Remove the cap from the new filter and check that the O-rings are in place.", "Align the new filter with the opening and push it in, then turn it clockwise until it stops or clicks into place.", "Close the cover and reset the filter indicator light (see your brand's reset guide).", "Flush the new filter by running water through the dispenser for the amount recommended in your manual, usually a few gallons."])],
  [("Do I need to turn off the water to change the filter?", "Most internal refrigerator filters do not require shutting off the water. Follow your manual; some models ask you to turn the water supply valve off first."),
   ("Why does the water sputter after the change?", "Air trapped in the line. Keep running water through the dispenser until the stream is steady and clear."),
   ("Can I change the filter myself?", "Yes. It is designed to be a homeowner task and needs no tools.")],
  steps=["Locate the old filter and open the cover if there is one.", "Turn the filter counterclockwise or press the release button and pull it straight out.", "Remove the protective cap from the new filter and check the O-rings.", "Align the new filter, push it in and turn it clockwise until it locks.", "Close the cover and reset the filter indicator light.", "Flush the filter by running water through the dispenser as recommended in the manual."],
  related=["how-to-flush-a-new-refrigerator-water-filter", "reset-refrigerator-water-filter-light"])

g("how-to-flush-a-new-refrigerator-water-filter",
  "How to Flush a New Refrigerator Water Filter (How Many Gallons?)",
  "After installing a new refrigerator water filter, flush it to remove air and carbon dust. Here is how long to run the dispenser and what to expect.",
  "How to flush a new refrigerator water filter",
  "A new carbon filter contains fine carbon dust and trapped air. Flushing clears both so the first glass of water is clear and tastes right.",
  [("What to do", ["Place a large pitcher or container under the dispenser and run water until the flow is steady. Most manufacturers ask for a few gallons; your manual gives the exact amount for your model.", "Do this in short bursts if the dispenser has an automatic timeout: pressing the lever, releasing it and repeating is normal."]),
   ("What you may see", ["Sputtering or spitting in the first few seconds is trapped air.", "Gray or cloudy water at first can be fine carbon particles. It should clear after flushing.", "If the water stays cloudy or particles keep coming, stop and check that the filter is seated correctly."]),
   ("Do not forget the ice", ["Ice made before the filter change can hold old taste. Discard the first batches of ice after changing the filter."])],
  [("How many gallons should I flush?", "It depends on the brand and model. Many guides ask for about 2 to 4 gallons of water, but check your owner's manual."),
   ("Is the first water safe to drink?", "Follow the filter and refrigerator manufacturers' instructions. Flushing is meant to be done before regular use."),
   ("Do I need to flush the ice maker too?", "Discard the first few batches of ice after a filter change so any residual taste or carbon dust clears out.")],
  related=["how-to-change-a-refrigerator-water-filter", "refrigerator-water-tastes-bad-after-changing-the-filter"])

g("reset-refrigerator-water-filter-light",
  "How to Reset the Refrigerator Water Filter Light (Samsung, LG, Whirlpool, GE)",
  "How to reset the water filter indicator light on Samsung, LG, Whirlpool and GE refrigerators after changing the filter.",
  "How to reset the refrigerator water filter light",
  "After you change the filter, the indicator light does not turn off by itself on most refrigerators: you have to reset it. The method is similar across brands, but the button name differs.",
  [("Samsung", [BRANDS["samsung"]["reset"]]), ("LG", [BRANDS["lg"]["reset"]]), ("Whirlpool, Maytag, KitchenAid", [BRANDS["whirlpool"]["reset"]]), ("GE", [BRANDS["ge"]["reset"]]),
   ("If the light stays on", ["Make sure the new filter is fully seated and turned to the locked position. Some models will not clear the light until the filter is detected.", "Check the manual for your exact model: touch-display models usually reset the filter from a settings menu."])],
  [("Why is my water filter light still on after replacing the filter?", "The reset may not have registered, or the filter may not be fully seated. Press and hold the reset button again and check that the filter is locked in."),
   ("Does resetting the light change how the filter works?", "No. The light only restarts the reminder timer or gallon counter."),
   ("What if my refrigerator has no reset button?", "Some models reset automatically when the new filter is detected. Check your owner's manual for the exact behavior.")],
  related=["how-to-change-a-refrigerator-water-filter"])

for key in ("samsung", "lg", "whirlpool", "ge"):
    b = BRANDS[key]["name"]
    g(f"{key}-refrigerator-water-filter-guide",
      f"{b} Refrigerator Water Filter Guide: Which Filter Fits Your Model?",
      f"A simple guide to {b} refrigerator water filters: part numbers, how to find yours, how to replace it and how to reset the filter light.",
      f"{b} refrigerator water filters: which one do you need?",
      f"{b} uses several different water filter designs, and a filter that looks similar is not always the right one. The quickest way to choose correctly is to start from your refrigerator model number or the part number on your old filter.",
      [("Start with the model number", [f"Find the model number on the label inside the refrigerator (see our guide on where it is). Then check the compatibility list on each {b} filter page, or use the finder."]),
       ("Match the part number", [f"Each filter below lists its main part number and the other numbers it is also known by. If your old filter or manual shows any of those, you are in the right place."]),
       ("Internal or external filter?", [f"Most {b} refrigerators use an internal cartridge. An external inline filter is an alternative for some dispenser models that do not have an internal filter."]),
       ("Replacing and resetting", [f"{b} filters are usually replaced about every six months. {BRANDS[key]['reset']}"])],
      [(f"How do I know which {b} filter I need?", f"Use the model number inside your refrigerator or the part number printed on the old filter. If you are unsure, send us a photo on WhatsApp."),
       (f"How often should I change my {b} water filter?", "About every six months, or sooner if water flow slows or the taste changes."),
       (f"Do all {b} refrigerators use the same filter?", "No. Different models use different filters, so always confirm with your model number.")],
      brand=key, related=["how-to-find-your-refrigerator-model-number", "reset-refrigerator-water-filter-light"])

g("refrigerator-water-tastes-bad-after-changing-the-filter",
  "Refrigerator Water Tastes Bad After Changing the Filter? Causes and Fixes",
  "If your fridge water tastes or smells odd after a filter change, the cause is usually trapped air, carbon dust or old ice. Here is what to try.",
  "Refrigerator water tastes bad after changing the filter",
  "A fresh filter should make water taste better, not worse. When it does not, there is usually a simple reason, and it is easy to fix.",
  [("Common causes", ["The new filter has not been flushed enough. Carbon dust and trapped air can affect the first glasses.", "Old water is still in the dispenser line or the water tank. It takes several gallons to clear.", "Old ice in the ice bin holds the previous taste. Empty the bin and let the ice maker produce new ice.", "The filter is not fully seated, so some water bypasses it.", "The water supply itself has a taste or odor that the filter is not handling."]),
   ("What to do", ["Flush another few gallons through the dispenser.", "Discard all the old ice and the first two batches of new ice.", "Take the filter out and reinstall it, making sure it turns fully until it locks.", "If the taste persists, check that the filter is the correct part number for your model."])],
  [("How long until the water tastes normal?", "Usually right after flushing and discarding the old ice. If it does not improve in a day, reinstall the filter."),
   ("Could I have installed the wrong filter?", "A wrong filter often will not fit, leaks or does not lock. Confirm the part number for your model.")],
  related=["how-to-flush-a-new-refrigerator-water-filter"])

g("refrigerator-water-filter-wont-twist-off",
  "Refrigerator Water Filter Stuck? How to Remove It Without Breaking It",
  "A stuck refrigerator water filter is common. Try these safe tips to loosen it and what to avoid.",
  "What to do when a refrigerator water filter is stuck",
  "Old filters can seal tightly into the housing. Force is the wrong approach: it can crack the filter head or the housing.",
  [("Try this first", ["Make sure you are turning in the right direction. Most filters turn counterclockwise to release; some push in and pop out.", "Check whether there is a release button or tab you must press or hold.", "Wear a rubber glove or hold a rubber jar-opener against the filter for extra grip.", "Turn off the water supply for a minute to reduce pressure, then try again."]),
   ("Avoid", ["Pliers or wrenches that can crack the plastic.", "Pulling straight out while twisting: a gentle, steady turn works better."]),
   ("If it still will not budge", ["Wait a few minutes and try again, or consult the manual for your model's release procedure. If the housing is cracked, stop and get help before using the dispenser."])],
  [("Is it normal for the filter to be hard to turn?", "A little resistance is normal on an old filter. Heavy resistance means something is wrong: stop and check the manual."),
   ("Will a new filter be easier to install?", "Yes. A new filter's O-rings are lubricated and the housing is clean, so it should turn smoothly.")],
  related=["how-to-change-a-refrigerator-water-filter"])

g("refrigerator-water-dispenser-slow-or-low-flow",
  "Refrigerator Water Dispenser Slow? Low Water Flow Causes",
  "If your refrigerator water dispenser is slow or the flow is weak, a clogged filter is the most common cause. Here is how to check.",
  "Why is my refrigerator water dispenser slow?",
  "Weak flow from the dispenser is almost always caused by a clogged filter. It is also the easiest thing to check.",
  [("Check in this order", ["The filter. If it has been more than six months, replace it and see if the flow improves.", "The filter cap or bypass plug. If you are not using a filter, make sure the bypass is installed correctly.", "The water line. Look for a kink behind the refrigerator.", "The shut-off valve to the refrigerator. Make sure it is fully open.", "Frozen line. A partially frozen water line can slow flow: check if the freezer or the fresh-food compartment is too cold."]),
   ("After changing the filter", ["Run several gallons through the dispenser. Air in the system can make the flow look weak for a while."])],
  [("Can a new filter fix low water pressure?", "Often yes. A clogged filter restricts flow. If a new filter does not help, the problem is elsewhere in the water line."),
   ("Should I run a filter bypass?", "A bypass plug restores flow but removes filtration. Use it only temporarily.")],
  related=["how-often-to-change-a-refrigerator-water-filter"])

g("refrigerator-water-filter-leaking",
  "Refrigerator Water Filter Leaking? Common Causes and Fixes",
  "A leaking refrigerator water filter is usually not seated, has a damaged O-ring or is the wrong part. Here is how to troubleshoot it.",
  "Refrigerator water filter leaking: what to check",
  "A leak around the filter is a sign that something is not sealing. Stop using the dispenser until you find out why.",
  [("Possible causes", ["The filter is not fully inserted or turned to the locked position.", "An O-ring is missing, twisted or damaged. Check the new filter before installing it.", "The filter is not the correct part number for the model.", "The housing is cracked or the water line fitting is loose.", "The filter was cross-threaded when installed."]),
   ("What to do", ["Turn off the water supply, remove the filter and inspect the O-rings and the housing.", "Reinstall the filter, aligning it carefully and turning only until it locks. Do not over-tighten.", "If it still leaks, the part may not be the right one for your refrigerator: confirm the part number or message us a photo."])],
  [("Is a small drip normal?", "A little water when you remove the old filter is normal. A continuing leak after installation is not."),
   ("Can I use Teflon tape on the filter?", "No. Refrigerator filters seal with O-rings, not thread tape.")],
  related=["how-to-find-your-refrigerator-model-number"])

g("do-you-need-a-refrigerator-water-filter",
  "Do You Need a Refrigerator Water Filter? Can You Use a Bypass Plug?",
  "Is a refrigerator water filter necessary? What it does, what a bypass plug is and when to replace the filter.",
  "Do you need a refrigerator water filter?",
  "Most refrigerators with a water dispenser or an ice maker are designed to use a filter, but they can run with a bypass plug instead. Whether you should depends on your water.",
  [("What the filter does", ["A typical refrigerator water filter reduces sediment and chlorine taste and odor. Some filters are certified for additional contaminants: check the filter's own certification information if that matters to you.", "A filter helps the dispenser and ice maker produce water and ice with a cleaner taste, and it helps keep sediment out of the lines."]),
   ("Bypass plug", ["A bypass plug fits in place of the filter. Water flows, but it is not filtered. Some refrigerators will show a filter alarm until the plug is installed or the reset is done."]),
   ("When to keep a filter", ["Well water, water with strong taste or odor, or visible sediment are good reasons to use a filter and change it on schedule.", "If you are concerned about water safety, a refrigerator filter is not a substitute for treatment. Follow local water quality advice."])],
  [("Can I run my refrigerator without a filter?", "Yes, with a bypass plug in most models, but water and ice will not be filtered."),
   ("Is a filter required for the ice maker?", "Not usually, but the filter improves ice taste and helps protect the ice maker from sediment.")],
  related=["how-often-to-change-a-refrigerator-water-filter"])

g("internal-vs-external-refrigerator-water-filters",
  "Internal vs External Refrigerator Water Filters: Which Is Better?",
  "Internal cartridges vs external inline filters for refrigerators: differences, installation and when to choose each.",
  "Internal vs external refrigerator water filters",
  "Most refrigerators use an internal cartridge, but an external inline filter on the water line is another way to filter water for the dispenser and ice maker.",
  [("Internal cartridge", ["Sits inside the refrigerator in a dedicated housing. It is designed for your model and is easy to change: twist or push, remove and replace."]),
   ("External inline filter", ["Mounts on the water line outside the refrigerator. It is useful for dispenser models without an internal filter housing and for ice makers. It is a bit more involved to install because you connect it to the water line."]),
   ("Which to choose", ["If your refrigerator has an internal filter housing, use the filter designed for it. Choose an external filter when there is no internal option or when you want to filter the supply to the ice maker."])],
  [("Can I use both?", "Some people do, but check your refrigerator's manual and the filters' instructions."),
   ("Do external filters need a tool to install?", "Usually they connect with push-in fittings or compression fittings. Follow the filter's instructions.")],
  related=["how-to-change-a-refrigerator-water-filter"])

g("what-do-nsf-ansi-42-53-and-401-mean",
  "What Do NSF/ANSI 42, 53 and 401 Mean on a Refrigerator Water Filter?",
  "A plain-English explanation of the NSF/ANSI standards you see on refrigerator water filter packaging.",
  "What do NSF/ANSI 42, 53 and 401 mean?",
  "Filter packaging often lists NSF/ANSI numbers. They are third-party standards that describe what a filter has been tested to reduce. Here is what the common ones mean.",
  [("NSF/ANSI 42", ["Covers aesthetic effects: chlorine taste and odor and particulates."]),
   ("NSF/ANSI 53", ["Covers health effects: certain contaminants such as lead, cysts, and others that depend on the product."]),
   ("NSF/ANSI 401", ["Covers some emerging contaminants, such as certain pharmaceuticals and other compounds."]),
   ("NSF/ANSI P473 and others", ["Some standards cover specific substances such as PFOA and PFOS. Which standards a particular filter meets is stated by the filter's manufacturer on the packaging."]),
   ("How to use this", ["Look at the claims and certifications printed on the specific filter you are buying. Do not assume two filters that look alike have the same certifications."])],
  [("Does every refrigerator filter have an NSF certification?", "No. Certifications are product-specific. Check the packaging of the filter you are considering."),
   ("Is an NSF mark a guarantee for all contaminants?", "No. A certification applies only to the substances and conditions listed in the standard and the product's performance data sheet.")],
  related=["do-you-need-a-refrigerator-water-filter"])

g("how-to-tell-which-refrigerator-water-filter-fits",
  "How to Tell Which Refrigerator Water Filter Fits Your Fridge",
  "Four ways to find the right refrigerator water filter: model number, old filter part number, shape and the owner's manual.",
  "How to tell which refrigerator water filter fits",
  "Refrigerator filters look alike but are not interchangeable. These four checks get you to the right one.",
  [("1. Use the refrigerator model number", ["Find the label inside the fridge and enter the number in our filter finder, or compare it with the model list on each filter page."]),
   ("2. Use the old filter's part number", ["Look at the end of the old filter. A code like DA29-00020B, LT700P, EDR1RXD1 or MWF identifies it."]),
   ("3. Compare the shape", ["Hold the old filter next to a photo: length, the top connector shape and how it locks in all matter."]),
   ("4. Read the manual", ["The manual names the filter part number for your model."]),
   ("Still not sure?", ["Send a photo of the old filter and the label inside the refrigerator to us on WhatsApp and we will help match it."])],
  [("Are different brands' filters interchangeable?", "Generally no. Each refrigerator is designed for specific filter designs."),
   ("What if two filters look identical?", "Compare the part numbers. Small differences in the top fitting can make a filter not lock or leak.")],
  related=["how-to-find-your-refrigerator-model-number"])

g("water-filter-light-stays-on-after-changing-filter",
  "Refrigerator Water Filter Light Stays On After Changing the Filter",
  "The filter light is still on even though you changed the filter? Check that you reset it, that the filter is locked and what else to try.",
  "Water filter light stays on after changing the filter",
  "This is a common issue. The light is usually a reminder timer, so it has to be reset manually, and the filter has to be properly seated.",
  [("Check these", ["You pressed and held the reset button for the right length of time (about 3 seconds on many models).", "The filter is fully inserted and turned to the locked position.", "The cover or door of the filter compartment is closed.", "The refrigerator's control panel is not in a mode that blocks the reset (check the manual).", "The filter is the correct part number. Some refrigerators detect the filter."]),
   ("If nothing works", ["Unplug the refrigerator for a few minutes and try again, or contact the manufacturer's support for your model."])],
  [("Does the light mean the filter is bad?", "No. It is a reminder based on time or gallons."),
   ("Can I ignore the light?", "You can, but it is a useful reminder to change the filter every six months.")],
  related=["reset-refrigerator-water-filter-light"])

g("refrigerator-ice-maker-cloudy-ice-or-bad-smell",
  "Cloudy Ice or Smelly Ice From the Refrigerator? Check the Water Filter",
  "Cloudy ice, strange taste or smell in refrigerator ice often points to an old filter or old ice. Here is what to do.",
  "Cloudy ice or smelly ice from the refrigerator",
  "Ice absorbs odors easily, and it holds the taste of whatever water and air it was made with. A worn-out filter is a common cause.",
  [("Possible causes", ["The water filter is overdue for replacement.", "Old ice has been sitting in the bin for a long time.", "Strong-smelling food in the freezer, especially if it is uncovered.", "Mineral content in the water: cloudy ice can come from dissolved air and minerals."]),
   ("What to do", ["Replace the filter and flush it.", "Empty the ice bin, wash it and let the ice maker make fresh ice.", "Keep foods covered in the freezer."])],
  [("Is cloudy ice a sign the filter is bad?", "Not always. Cloudy ice can be due to air and minerals. A bad taste or odor is more likely connected to the filter."),
   ("How often should I clean the ice bin?", "Every few months, or whenever the ice has an off taste.")],
  related=["how-often-to-change-a-refrigerator-water-filter"])

g("refrigerator-water-filter-vs-pitcher-vs-under-sink",
  "Refrigerator Filter vs Pitcher vs Under-Sink Filter: What to Choose",
  "Compare a refrigerator water filter with a pitcher filter and an under-sink system: convenience, cost and what to consider.",
  "Refrigerator filter vs pitcher vs under-sink filter",
  "All three can improve water taste. The right choice depends on what you want to filter and where.",
  [("Refrigerator filter", ["Convenient: filtered water and ice at the door without extra steps. Limited to the dispenser and ice maker, and designed for a specific refrigerator model."]),
   ("Pitcher filter", ["Inexpensive and portable. You have to refill it and it filters small amounts at a time."]),
   ("Under-sink filter", ["Filters water at a dedicated faucet for the whole kitchen's drinking needs. Requires installation."]),
   ("How to choose", ["If your goal is better tasting water and ice from your refrigerator, replace its filter on time. If you have a specific water quality concern, look for a filter certified for that contaminant and consider testing your water."])],
  [("Is the refrigerator filter enough?", "For taste and odor, often yes. For specific contaminants, check the filter's certifications."),
   ("Can I use a pitcher and the refrigerator filter together?", "You can, but it is not necessary for most households.")],
  related=["what-do-nsf-ansi-42-53-and-401-mean"])

g("can-you-use-a-refrigerator-without-a-water-filter",
  "Can You Use a Refrigerator Without a Water Filter? What Happens",
  "What happens if you run your refrigerator without a water filter, and how to use a bypass plug safely.",
  "Can you use a refrigerator without a water filter?",
  "Yes, in most refrigerators you can, as long as the filter slot is not left open. Water will not flow without either a filter or a bypass plug.",
  [("What happens", ["The dispenser and ice maker will work normally with a bypass plug installed.", "Water and ice are not filtered, so taste and odor may be less pleasant, and sediment can reach the ice maker."]),
   ("How to do it", ["Use the bypass plug supplied by the manufacturer for your model. If you do not have one, order the correct plug or filter for your refrigerator."]),
   ("Keep in mind", ["Do not leave the filter slot empty: water will not flow and some models will leak."])],
  [("Is the bypass plug the same for all refrigerators?", "No. Each model uses its own plug design."),
   ("Will the filter light turn off with a bypass plug?", "Some models need a reset; check your manual.")],
  related=["do-you-need-a-refrigerator-water-filter"])

SLUGS = [x["slug"] for x in G]
