;;; Code, that should be evaluated, when emacs is called

(defun leo-lookup ()
  "Look up current word in LEO in a browser.

If a region is active (a phrase), lookup that phrase."
  (interactive)
  (let (myWord myUrl)
    (setq myWord
          (if (region-active-p)
              (buffer-substring-no-properties (region-beginning) (region-end))
            (thing-at-point 'symbol)))
    (setq myUrl
          (concat "http://dict.leo.org/#/search=" myWord))
    (browse-url myUrl)))
