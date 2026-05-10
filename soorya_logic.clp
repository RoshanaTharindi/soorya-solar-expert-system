(deftemplate user-data
   (slot monthly-units (type INTEGER))
   (slot primary-goal (type SYMBOL))
   (slot budget (type SYMBOL)))

(deftemplate recommendation
   (slot scheme (type STRING))
   (slot reasoning (type STRING)))

;; ---------------------------------------------------------
;; RULE 1: Net Metering (User just wants to offset bill)
;; ---------------------------------------------------------
(defrule net-metering
   (user-data (primary-goal offset-bill))
   =>
   (assert (recommendation 
      (scheme "Net Metering") 
      (reasoning "Best for offsetting domestic bills using CEB credits (carried forward for 10 years)."))))

;; ---------------------------------------------------------
;; RULE 2: Net Accounting Viable (Low/Med Budget, Low Usage)
;; ---------------------------------------------------------
(defrule net-accounting-viable
   (user-data (primary-goal generate-income) (budget ?b) (monthly-units ?u))
   (test (or (eq ?b medium) (eq ?b low)))
   (test (< ?u 300)) ; Smart check: Usage is low enough to generate excess
   =>
   (assert (recommendation 
      (scheme "Net Accounting") 
      (reasoning "Your consumption is low enough to generate excess power. You will earn Rs. 22.00 per excess unit sold to the grid."))))

;; ---------------------------------------------------------
;; RULE 3: Net Accounting Warning (Low/Med Budget, High Usage)
;; ---------------------------------------------------------
(defrule net-accounting-warning
   (user-data (primary-goal generate-income) (budget ?b) (monthly-units ?u))
   (test (or (eq ?b medium) (eq ?b low)))
   (test (>= ?u 300)) ; Smart check: Usage too high for budget
   =>
   (assert (recommendation 
      (scheme "Net Metering (Strongly Advised)") 
      (reasoning "Your usage (>300 kWh) is too high for a small solar array to generate profit. Focus on offsetting your high monthly bills first."))))

;; ---------------------------------------------------------
;; RULE 4: Net Plus (High Budget)
;; ---------------------------------------------------------
(defrule net-plus
   (user-data (primary-goal generate-income) (budget high))
   =>
   (assert (recommendation 
      (scheme "Micro Solar Power Producer (Net Plus)") 
      (reasoning "With a high budget, you can install a dedicated export meter. The CEB buys 100% of your generated power."))))

;; ---------------------------------------------------------
;; RULE 5: Catch-All Fallback
;; ---------------------------------------------------------
(defrule fallback
   (declare (salience -10))
   (not (recommendation (scheme ?)))
   =>
   (assert (recommendation 
      (scheme "Custom CEB Consultation") 
      (reasoning "Your specific input parameters require a custom site assessment by a registered SLSEA service provider."))))