# The standalone IDE/CLI version

(deftemplate user-data
   (slot monthly-units (type INTEGER))
   (slot primary-goal (type INTEGER))
   (slot budget (type INTEGER)))

;; --- 1. USER-FRIENDLY INPUT RULE ---
(defrule ask-questions
   (not (user-data))
   =>
   (printout t "--- 🇱🇰 Soorya Bala Sangramaya Expert System ---" crlf crlf)
   
   ;; Added (kWh) as requested
   (printout t "1. What is your average monthly electricity consumption (in kWh)? ")
   (bind ?u (read))
   
   ;; Changed to Numbered Menu for Goals
   (printout t crlf "2. What is your primary goal?" crlf)
   (printout t "   [1] - Offset my monthly bill" crlf)
   (printout t "   [2] - Generate extra income" crlf)
   (printout t "   Enter 1 or 2: ")
   (bind ?g (read))
   
   ;; Changed to Numbered Menu with LKR Brackets for Budget
   (printout t crlf "3. What is your upfront investment budget?" crlf)
   (printout t "   [1] - Low (< 800,000 LKR)" crlf)
   (printout t "   [2] - Medium (800,000 LKR - 1,500,000 LKR)" crlf)
   (printout t "   [3] - High (> 1,500,000 LKR)" crlf)
   (printout t "   Enter 1, 2, or 3: ")
   (bind ?b (read))
   
   (assert (user-data (monthly-units ?u) (primary-goal ?g) (budget ?b))))

;; --- 2. LOGIC RULES ---

;; If they just want to offset their bill (Goal 1)
(defrule net-metering
   (user-data (primary-goal 1))
   =>
   (printout t crlf ">>> EXPERT RESULT: NET METERING" crlf)
   (printout t "REASON: You selected Goal 1. This scheme allows you to carry forward excess energy as credits for up to 10 years to offset future domestic bills." crlf))

;; USING MONTHLY UNITS: Income goal, Low/Med Budget, LOW consumption
(defrule net-accounting-viable
   (user-data (primary-goal 2) (budget ?b) (monthly-units ?u))
   (test (or (= ?b 1) (= ?b 2)))
   (test (< ?u 300)) ; System checks if units are low enough to have excess
   =>
   (printout t crlf ">>> EXPERT RESULT: NET ACCOUNTING" crlf)
   (printout t "REASON: With your budget and lower consumption (" ?u " kWh), your system will generate excess energy. CEB will pay you Rs. 22.00 per excess unit." crlf))

;; USING MONTHLY UNITS: Income goal, Low/Med budget, HIGH consumption
(defrule net-accounting-warning
   (user-data (primary-goal 2) (budget ?b) (monthly-units ?u))
   (test (or (= ?b 1) (= ?b 2)))
   (test (>= ?u 300)) ; System catches that usage is too high for a small system
   =>
   (printout t crlf ">>> EXPERT RESULT: NET METERING (STRONGLY ADVISED)" crlf)
   (printout t "REASON: You want income, but your usage (" ?u " kWh) is too high for a low/medium budget system to generate excess power. Focus on offsetting your bill first." crlf))

;; If they have a High Budget (Budget 3)
(defrule net-plus
   (user-data (primary-goal 2) (budget 3))
   =>
   (printout t crlf ">>> EXPERT RESULT: MICRO SOLAR POWER PRODUCER (NET PLUS)" crlf)
   (printout t "REASON: With a high budget (> 1.5M LKR), you can install a dedicated export meter. The CEB buys 100% of the electricity you generate." crlf))