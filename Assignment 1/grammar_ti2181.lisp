(defparameter *grammar*
  '(
    (Sentence -> (SNP SVP) (PNP PVP) (Sentence coordinate-conj Sentence) (Sub-conjunction sentence VP))
    ;Nouns and verbs
    (Noun -> SNP PNP)
    (VP -> SVP PVP)
    ;Singular nouns and verbs
    (SNP -> (SNoun) (SDet SNoun) (SNP PP) (SNP RelativeClause) (SPronoun))
    (SVP -> (SVerb) (AXP) (SVP SNP) (SVerb Adjective) (SVP PP) (SVP Adverb) (Adverb SVP) (SVP Infinitive))
    (SPronoun -> it)
    (SNoun -> (Adjective SNoun) education narrative polarization strategy intent business care asteroid eye prosecution case penalty) ;12
    (SVerb -> tend pay see)
    ;Plural nouns and verbs
    (PNP -> (PNoun) (PDet PNoun) (PNP PP) (PNP RelativeClause) (Noun ListConj Noun) (PPronoun)(PQuantifiers PNoun))
    (PVP -> (PVerb) (AXP) (PVP PNP) (PVerb Adjective) (PVP PP) (PVP Adverb) (Adverb PVP)(PVP Infinitive))
    (PPronoun -> There)
    (PNoun -> (Adjective PNoun) bananas gains industries services weeks telescopes scientists )
    (PVerb -> were play catch)  
    ;Preposition phrase
    (PP -> (Preposition SNP) (Preposition PNP))
    (Preposition -> (PrepDet DetPrep) of in to with)
    (PrepDet -> such)
    (DetPrep -> as) 
    ;Adjectives and adverbs
    (Adjective ->  (noun-adjunct) higher prevailing flawed desired solid several professional visible naked able few decided );12
    (noun-adjunct -> health job amateur death)
    (Adverb -> hardly well not)
    ;Determiners
    (Sdet -> a this the)
    (PDet -> these PQuantifiers )
    ;quantifiers
    (PQuantifiers -> (PQDet PQuant) PQuant)
    (PQDet -> a )
    (PQuant -> few couple)
    ;Auxilary verb phrase
    (AXP -> (AuxPro AuxVP) (AuxPro Adverb AuxVP) (AuxPro AuxVP Adjective) (AuxPro Adverb AuxVP Adjective))
    (AuxPro -> must mustnt will should)
    (AuxVP -> counter achieve be seek)
    ;Relative Clause
    (RelativeClause -> (Rel-conj SVP) (Rel-conj PVP))
    (Rel-conj -> that)
    ;Infinitive
    (infinitive -> (to SVerb) (to SVerb noun))
    ;Lists
    (ListConj -> and or)
    ;conjunctions
    (Sub-conjunction -> whether)
    (coordinate-conj -> and but yet or)
  )
  "A grammar for a trivial subset of English.")
(defun targeted-sentence (rules)
  (apply-rules rules nil)
)
;list of rules using DFS order
(defparameter rules1 '((Sentence 0)(SNP 0)(SNoun 0)(Adjective 1)(SNoun 1)(SVP 2)(SVP 1)(AXP 0)(AuxPro 0)
  (AuxVP 0)(SNP 2)(SNP 1)(SDet 2)(SNoun 0)(Adjective 2)(SNoun 2)(PP 0)(Preposition 1)(SNP 0)(SNoun 3))) 
(defparameter rules2 '((sentence 0)(SNP 1)(Sdet 1)(SNoun 0)(Adjective 3)(SNoun 4)(SVP 2)(SVP 1)(AXP 1)
  (AuxPro 2)(Adverb 0)(AuxVP 1)(SNP 1)(SDet 2)(SNoun 0)(Adjective 4)(SNoun 5)))
(defparameter rules3 '((Sentence 1)(PNP 5)(PPronoun 0)(PVP 2)(PVP 0)(PVerb 0)(PNP 3)(PNP 2)(PNP 0)(PNoun 0)(Adjective 5)(PNoun 0)
  (Adjective 0)(noun-adjunct 1)(PNoun 2)(PP 1)(Preposition 2)(PNP 0)(PNoun 0)(Adjective 6)(PNoun 3)(PNP 3)(RelativeClause 0)(Rel-conj 0)(SVP 4) 
  (SVP 5)(SVP 7)(SVP 0)(SVerb 0)(Infinitive 0)(SVerb 1)(Adverb 1)(PP 1)(Preposition 0)(PrepDet 0)(DetPrep 0)(PNP 4)(Noun 0)(SNP 0)
  (SNoun 6)(ListConj 0)(Noun 1)(PNP 4)(Noun 1)(PNP 0)(PNoun 0)(Adjective 7)(PNoun 4)(ListConj 0)(Noun 0)(SNP 0)(SNoun 0)(Adjective 0)(noun-adjunct 0)
  (SNoun 7)))   
(defparameter rules4 '((sentence 2)(sentence 0)(SNP 1)(SDet 2)(SNoun 8)(SVP 4)(SVP 1)(AXP 3)(AuxPro 2)(Adverb 2)(AuxVP 2)
(Adjective 8)(PP 0)(Preposition 3)(SNP 1)(Sdet 2)(Snoun 0)(Adjective 9)(Snoun 9)(coordinate-conj 1)(sentence 1)(PNP 0)(PNoun 0)
(Adjective 0)(noun-adjunct 2)(PNoun 7)(PVP 4)(PVP 7)(PVP 1)(AXP 2)(AuxPro 3)(AuxVP 2)(Adjective 10)(Infinitive 1)(SVerb 2)(Noun 0)(SNP 4)
(SPronoun 0)(PP 1)(Preposition 4)(PNP 0)(PNoun 6)))
(defparameter rules5 '((Sentence 3)(Sub-conjunction 0)(sentence 0)(SNP 1)(SDet 2)(SNoun 10)(SVP 4)(SVP 2)(SVP 1)(AXP 0)(AuxPro 2)
(AuxVP 3)(SNP 1)(SDet 2)(SNoun 0)(Adjective 0)(noun-adjunct 3)(SNoun 12)(PP 0)(Preposition 2)(SNP 1)(SDet 2)(SNoun 11)
(VP 0)(SVP 4)(SVP 1)(AXP 2)(AuxPro 2)(AuxVP 2)(Adjective 12)(PP 1)(Preposition 2)(PNP 6)(PQuantifiers 0)(PQDet 0)(PQuant 0)
(SNoun 0)(Adjective 11)(PNoun 5)))



(defun apply-rules (rules sentence)
  (cond 
    ((null rules) sentence)
    ((null sentence) (apply-rules (rest rules) (elt (rule-rhs (assoc (car (car rules)) *grammar*)) (second (car rules)))))
    (t (let ((rule-to-rewrite (car (car rules))) (new-rule (elt (rule-rhs (assoc (car (car rules)) *grammar*)) (second (car rules)))))
      (apply-rules (rest rules) (rewrite-sentence nil sentence rule-to-rewrite new-rule)))))) 

;simply rewrites a sentence replacing the first occurence of the variable "rule-to-rewrite" in "sentence-next" by the symbols in "new-rule" 
;example: (rewrite-sentence nil '(THE MAN verb-phrase) 'verb-phrase '(Verb noun-phrase))
;returns (THE MAN Verb noun-phrase)
(defun rewrite-sentence (sentence-pre sentence-next rule-to-rewrite new-rule)
    (cond ((null sentence-next) sentence-pre)
    (t 
      (if (equal (car sentence-next) rule-to-rewrite)
      (append (append sentence-pre (if (listp new-rule) new-rule (list new-rule))) (rest sentence-next))
      (rewrite-sentence (append sentence-pre (list (car sentence-next))) (rest sentence-next) rule-to-rewrite new-rule)))))
      

(defun random-elt (list)
  (elt list
       (random (length list))))

;global variable
(defvar depth 0)
(defvar test)

;Generate a random sentence or phrase
(defun generate-sentence (phrase)
  (setf depth 0)
  (setq sentence (random-sentence phrase))
  (if (null test)(generate-sentence phrase)(car (list sentence)) )
  )

;Generate a random sentence or phrase
(defun random-sentence (phrase) ;depth)
   (setf depth (+ 1 depth))
  (cond 
     ((> depth 60) (setf test nil))
    ((listp phrase)
         (mappend #'random-sentence phrase))
        ((rewrites phrase)
         (random-sentence (random-elt (rewrites phrase)))
         ; (setf depth (- depth 1)) 
         )
        (t
        (setf depth (- depth 1)) 
          (setq test (list phrase))
          ))
  ;(if t depth nil)
  )
; Generate a random sentence or phrase, with a complete parse tree.
(defun generate-tree (phrase)
  (cond ((listp phrase)
         (mapcar #'generate-tree phrase))
        ((rewrites phrase)
         (cons phrase
               (generate-tree (random-elt (rewrites phrase)))))
        (t (list phrase))))

; Append the results of calling fn on each element of list. Like mapcon, but uses append instead of nconc.
(defun mappend (fn list)
   (apply #'append (mapcar fn list)))

; The right hand side of a rule.
(defun rule-rhs (rule)
  (rest (rest rule)))
;Return a list of the possible rewrites for this category.
(defun rewrites (category)
  (rule-rhs (assoc category *grammar*)))
;generate sentence and write to q1
(defun run1 ()
  (let ((sent (generate-sentence  'sentence)))
    (write-to-file1 (if (validp sent) (format nil "~S ~%" sent) (format nil "~S ~%" sent)))))
;generate sentence and write to q2 with indicator of validity
(defun run2 ()
  (let ((sent (generate-sentence  'sentence)))
    (write-to-file2 (if (validp sent) (format nil "+ ~S ~%" sent) (format nil "- ~S ~%" sent)))))

;writes both files N many times
(defun loop-run (N)
  (loop for i from 1 to N do (run1))
  (loop for i from 1 to N do (run2)))

;writes file 1
(defun write-to-file1 (sentence)
  (with-open-file (str "q1_ti2181.txt"
                     :direction :output
                     :if-exists :append
                     :if-does-not-exist :create)
    (format str sentence)))

;writes file 2
(defun write-to-file2 (sentence)
  (with-open-file (str "q2_ti2181.txt"
                     :direction :output
                     :if-exists :append
                     :if-does-not-exist :create)
    (format str sentence)))

;generate the list of all possible words that can be repeated in a sentence
(defun generate_allowed_list()
  (setq allowrepeat (rewrites 'Sdet))
  (setq allowrepeat(append (rewrites 'coordinate-conj) allowrepeat))
  (push 'THESE allowrepeat)
  (push 'SUCH allowrepeat)
  (push 'AS allowrepeat)
  (loop for item in (rewrites 'Preposition)
    do
    (if (listp item)
      nil
      (progn
        (push item allowrepeat)
        )
     )
  )  
  (list allowrepeat)
  )

;takes an element and a list and returns true only if element is in the list
(defun checkmatchp(test checklist)
  (if (member test checklist) t nil)
  )

;checks a sentence for repeated words excluding prepositions, determiners and conjunctions
(defun checkduplicatesp (sentence)
  (setq allowrepeat (generate_allowed_list))
  (setq used '())
  (setq i 0)
  (setq bool t)
  (loop do
    (if (checkmatchp (nth i sentence) (car allowrepeat))
      nil
      (if (checkmatchp (nth i sentence) used)
        (progn
        (setq bool nil)
        )
        (push (nth i sentence) used)))
    (incf i)
   while (< i (list-length sentence)))
  (if t bool nil)
  )
;return true if length of sentence is less than 20
(defun checksizep (sentence)
  (if (< (list-length sentence) 40) t nil)
  )
;checks to see the number of prepositions doesnt exceed 5
(defun prepp (sentence)
  (setq prep (rewrites 'Preposition))
  (setq count 0)
  (loop do
    (if (checkmatchp (nth i sentence) prep)
      (incf count)
      (setq count 0)
      )
    (incf i)
   while (< i (list-length sentence)))
    (if t bool nil)
  )
  

;checks to see if there are 3 consecutive adjectives
(defun adjp(sentence)
  (setq adj (rewrites 'Adjective ))
  (setq count 0)
  (setq bool t)
  (loop do
    (if (> count 2) (setq bool nil) nil)
    (if (checkmatchp (nth i sentence) adj)
      (incf count)
      (setq count 0)
      )
    (incf i)
   while (< i (list-length sentence)))
    (if t bool nil)
  )



;return true if valid sentence
(defun validp (sentence)
  (setq bool (checksizep sentence)) 
  (setq bool1 (checkduplicatesp sentence)) 
  (setq bool (prepp sentence)) 
  (setq bool (adjp sentence)) 
  (if (and bool bool1) t nil)
  )

(defun generateValid (phrase)
  (setq sentence (generate-sentence phrase))
  (if (validp sentence)sentence(generateValid phrase))
  )


