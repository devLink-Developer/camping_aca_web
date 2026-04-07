(function () {
    const TRANSITION_MS = 220;

    function setPauseButtonState(button, paused) {
        if (!button) return;
        button.setAttribute('aria-pressed', paused ? 'true' : 'false');
        button.setAttribute('aria-label', paused ? 'Reanudar notificación' : 'Pausar notificación');
        button.innerHTML = paused
            ? '<i class="fas fa-play"></i>'
            : '<i class="fas fa-pause"></i>';
    }

    function initToast(toast) {
        if (!toast || toast.dataset.toastReady === 'true') return;
        toast.dataset.toastReady = 'true';

        const duration = Math.max(0, Number(toast.dataset.duration || 2000));
        const progress = toast.querySelector('[data-toast-progress]');
        const pauseButton = toast.querySelector('[data-toast-pause]');
        const closeButton = toast.querySelector('[data-toast-close]');
        const stack = toast.closest('[data-toast-stack]');

        let remaining = duration;
        let startedAt = 0;
        let timerId = null;
        let rafId = null;
        let paused = false;
        let manuallyPaused = false;
        let interactionPaused = false;
        let closing = false;

        const updateProgress = (value) => {
            if (!progress || duration <= 0) return;
            const ratio = Math.min(1, Math.max(0, value / duration));
            progress.style.transform = `scaleX(${ratio})`;
        };

        const clearTimers = () => {
            if (timerId) {
                window.clearTimeout(timerId);
                timerId = null;
            }
            if (rafId) {
                window.cancelAnimationFrame(rafId);
                rafId = null;
            }
        };

        const destroyIfEmpty = () => {
            if (!stack) return;
            if (stack.querySelector('[data-app-toast]')) return;
            stack.remove();
        };

        const closeToast = () => {
            if (closing) return;
            closing = true;
            clearTimers();
            toast.classList.remove('is-visible', 'is-paused');
            toast.classList.add('is-closing');
            window.setTimeout(() => {
                toast.remove();
                destroyIfEmpty();
            }, TRANSITION_MS);
        };

        const tick = () => {
            if (paused || closing) return;
            const elapsed = Date.now() - startedAt;
            const currentRemaining = Math.max(0, remaining - elapsed);
            updateProgress(currentRemaining);
            if (currentRemaining <= 0) {
                closeToast();
                return;
            }
            rafId = window.requestAnimationFrame(tick);
        };

        const syncPauseState = () => {
            const shouldPause = manuallyPaused || interactionPaused;

            if (closing) return;

            if (shouldPause) {
                if (!paused) {
                    paused = true;
                    remaining = Math.max(0, remaining - (Date.now() - startedAt));
                    clearTimers();
                    updateProgress(remaining);
                    toast.classList.add('is-paused');
                }
                setPauseButtonState(pauseButton, manuallyPaused);
                return;
            }

            if (!paused) return;
            if (remaining <= 0) {
                closeToast();
                return;
            }

            paused = false;
            toast.classList.remove('is-paused');
            startedAt = Date.now();
            setPauseButtonState(pauseButton, false);
            updateProgress(remaining);
            timerId = window.setTimeout(closeToast, remaining);
            rafId = window.requestAnimationFrame(tick);
        };

        const startToast = () => {
            if (closing) return;
            clearTimers();
            paused = false;
            startedAt = Date.now();
            setPauseButtonState(pauseButton, false);
            updateProgress(remaining);
            timerId = window.setTimeout(closeToast, remaining);
            rafId = window.requestAnimationFrame(tick);
        };

        pauseButton?.addEventListener('click', () => {
            manuallyPaused = !manuallyPaused;
            syncPauseState();
        });

        closeButton?.addEventListener('click', closeToast);

        toast.addEventListener('mouseenter', () => {
            interactionPaused = true;
            syncPauseState();
        });
        toast.addEventListener('mouseleave', () => {
            interactionPaused = toast.matches(':focus-within');
            syncPauseState();
        });
        toast.addEventListener('focusin', () => {
            interactionPaused = true;
            syncPauseState();
        });
        toast.addEventListener('focusout', () => {
            window.setTimeout(() => {
                interactionPaused = toast.matches(':hover') || toast.matches(':focus-within');
                syncPauseState();
            }, 0);
        });

        if (duration <= 0) {
            setPauseButtonState(pauseButton, true);
            pauseButton?.setAttribute('disabled', 'disabled');
        } else {
            startToast();
        }

        window.requestAnimationFrame(() => {
            toast.classList.add('is-visible');
        });
    }

    function initAllToasts() {
        document.querySelectorAll('[data-app-toast]').forEach(initToast);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAllToasts);
    } else {
        initAllToasts();
    }
})();
