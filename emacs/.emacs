(setq load-path       (cons "/home/klulrich/lib/emacs/egg" load-path))
(setq load-path       (cons "/home/klulrich/lib/emacs/pmr" load-path))

(require 'egg)
(require 'pmr-template)

;; copy and past behavior
(setq x-select-enable-clipboard t) ; as above
(setq interprogram-paste-function 'x-cut-buffer-or-selection-value)

;;; Do not use new window
(setq ediff-window-setup-function 'ediff-setup-windows-plain)

;;; reread file if modified
(global-auto-revert-mode 1)

;;; Global key bindings
(define-key global-map [f1] 'manual-entry)	; Druck = Manualpage
(define-key global-map [f2] 'todo-show)	; Druck = Manualpage
(define-key global-map [f8] 'point-to-register) ; F8 - Punkt merken
(define-key global-map [f9] 'register-to-point) ; F9 - Punkt anspringen
;(define-key global-map [f10] 'revert-buffer)    ; F10 - reread file
(define-key global-map "\C-x\C-b" 'electric-buffer-list)
;; Find-File-at-Point package
(require 'ffap)                      ; load the package
(ffap-bindings)                      ; do default key bindings

(auto-compression-mode 1)

(diary 5)

(show-paren-mode 1)

;; insert PMR template
;(fset 'PMR-insert-template
;   [escape ?x ?i ?n ?s ?e tab ?f tab return ?W ?i ?s ?s ?e ?n ?/ ?P ?M ?R ?_ ?t ?e ?m ?p ?l ?a ?t ?e ?. ?t ?x ?t return])
;(global-set-key [f12] (quote PMR-insert-template))

;(fset 'pmr-text-butify
;   [?\C-s ?W ?a ?i ?t ?  ?f ?o ?r ?  ?c ?u ?s ?t ?o ?m ?e ?r ?\C-m ?\C-n ?\C-a ?\C-  C-end ?\C-w C-home ?\C-s ?A ?C ?T ?I ?O ?N ?  ?T ?A ?K ?E ?N ?\C-s ?\C-m ?\C-a ?\C-  C-home ?\C-w ?\C-x ?\C-s])

;; remove trailing space
;(fset 'pmr-remove-trailing-space
;   [?\C-e escape ?\\ ?\C-n ?\C-a])
;(global-set-key [f11] 'pmr-remove-trailing-space)

;; remove @37
;(fset 'pmr-remove-at37
;   [?\C-e ?\C-r ?\C-q tab ?\C-m ?\C-k ?\C-n ?\C-a])
;(global-set-key [f10] 'pmr-remove-at37)

(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(inhibit-startup-screen t)
 '(safe-local-variable-values (quote ((todo-categories "Todo")))))
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )

