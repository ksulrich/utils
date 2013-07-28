;;; see http://ergoemacs.org/emacs/elisp.html

;; idiom for string replacement in whole buffer

(let ((case-fold-search t)) ; or nil
  (goto-char (point-min))
  (while (search-forward "myStr" nil t)
    (replace-match "myReplaceStr" t t)))

;; for regex, use search-forward-regex

;myStr1 myStr2

(setq text (buffer-string))
(buffer-file-name)


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


(defun select-inside-quotes ()
  "Select text between double straight quotes
on each side of cursor."
  (interactive)
  (let (p1 p2)
    (skip-chars-backward "^\"")
    (setq p1 (point))
    (skip-chars-forward "^\"")
    (setq p2 (point))

    (goto-char p1)
    (push-mark p2)
    (setq mark-active t)
  )
)

(defun dosomething-region (p1 p2)
  "Prints region starting and ending positions." 
  (interactive "r")
  (message "Region starts: %d, end at: %d" p1 p2)
)

(defun query-friend-name (x)
  "inline doc string"
  (interactive "sEnter friend's name: ")
  (message "Name: %s" x)
)

(defun query-user (x y)
  "…"
  (interactive "sEnter friend's name: \nnEnter friend's age: ")
  (message "Name is: %s, Age is: %d" x y)
)

(defun ff (arg)
  "Prompt user to enter a string, with input history support."
  (interactive (list (read-string "Your name is:")) )
  (message "String is 「%s」." arg) )

; idiom for calling a shell command and get its output
(shell-command-to-string "ls")

(princ "current stack2: " )
