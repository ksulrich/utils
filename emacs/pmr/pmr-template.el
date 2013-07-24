;;; 
;;; PMR template related functions
;;;

(defconst pmr-template-version "0.0.1")

;;
;; Open ~/x.txt and insert PMR template
;; Position cuser in received email section
;;
(defun pmr-read-template ()
  (interactive)
  (find-file "~/x.txt")
  (goto-char 0)
  (insert-file-contents "~/Wissen/PMR_template.txt")
  (point-min)
  (search-forward "ACTION TAKEN:")
  (search-forward "---------------------------- EMAIL TEXT START --------------------------")
  (next-line))

;(pmr-read-template)
;;
;; Do clean-up steps and save buffer
;;
(defun pmr-clean-up ()
  (interactive)
  (save-excursion
    (find-file "~/x.txt")
    (goto-char (point-min))
    (re-search-forward "\\*+LotusCRT02\\*+")
    (delete-region (point) (point-max))
    (goto-char (point-min))
    (replace-regexp "\tPage [0-9]+ of [0-9]+" "")
    (save-buffer)))


;(pmr-clean-up)

(define-key global-map [f12] 'pmr-read-template)
(define-key global-map [f11] 'pmr-clean-up)