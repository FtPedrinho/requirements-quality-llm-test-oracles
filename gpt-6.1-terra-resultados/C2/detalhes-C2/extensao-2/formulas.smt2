; Y001
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert A)
(assert (distinct "one" "two"))
(model-add A () Bool true)

(check-sat)
(get-model)
; Y002
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert A)
(assert (not A))

(check-sat)
; Y003
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert A)
(assert (distinct "one" "one"))

(check-sat)
; Y004
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert A)
(assert (= "x" "y"))

(check-sat)
; Y005
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert (or A (not A)))
(assert (not A))
(model-add A () Bool false)

(check-sat)
(get-model)
; Y006
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert (or A (not A)))
(assert (not (or A (not A))))

(check-sat)
; Y007
(reset)
(set-option :timeout 60000)
(declare-fun A () Bool)
(assert A)
(assert (not A))

(check-sat)
; Y008
(reset)
(set-option :timeout 60000)
(declare-fun speed () Real)
(assert (> speed 100.0))
(assert (> speed 50.0))
(model-add speed () Real 101.0)

(check-sat)
(get-model)
; Y009
(reset)
(set-option :timeout 60000)
(declare-fun speed () Real)
(assert (> speed 100.0))
(assert (not (> speed 50.0)))

(check-sat)
; Y010
(reset)
(set-option :timeout 60000)
(declare-fun speed () Real)
(assert (not (> speed 100.0)))
(assert (> speed 50.0))
(model-add speed () Real 51.0)

(check-sat)
(get-model)
; Y011
(reset)
(set-option :timeout 60000)
(declare-fun speed () Real)
(assert (not (> speed 100.0)))
(assert (not (> speed 50.0)))
(model-add speed () Real 0.0)

(check-sat)
(get-model)
