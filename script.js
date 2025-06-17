// Landing page functionality
document.addEventListener('DOMContentLoaded', function () {
    // Check which page we're on
    if (document.querySelector('.landing-page')) {
        setupLandingPage();
    } else if (document.querySelector('.tutors-page')) {
        setupTutorsPage();
    }
});

function setupLandingPage() {
    // Typewriter effect
    const textElement = document.getElementById('typewriter-text');
    const text = "LearnzVerse is an AI-powered homework assistant designed to help students understand and complete assignments across core subjects. Featuring four virtual tutors—Mr. Newton (Physics), Madam Curie (Chemistry), Dr. Darwin (Biology), and Prof. Euler (Math)—our app provides personalized, concept-based explanations tailored to your class level.";

    let charIndex = 0;
    let currentText = '';

    function type() {
        if (charIndex < text.length) {
            currentText += text.charAt(charIndex);
            textElement.textContent = currentText;
            charIndex++;
            setTimeout(type, 30);
        } else {
            // Add cursor after typing completes
            textElement.innerHTML += '<span class="cursor">|</span>';
        }
    }

    // Start typing after a short delay
    setTimeout(type, 1000);

    // Canon click event
    const canon = document.getElementById('canon');
    const cannonBall = document.getElementById('cannon-ball');

    canon.addEventListener('click', function () {
        // Hide the "Click Me" text
        document.querySelector('.click-me').style.opacity = '0';

        // Animate the cannon ball
        cannonBall.style.opacity = '1';
        cannonBall.style.animation = 'shoot 1.5s forwards';

        // After animation completes, navigate to tutors page
        setTimeout(function () {
            // Animate the background logo explosion
            const backgroundLogo = document.querySelector('.background-logo');
            backgroundLogo.style.animation = 'explode 0.5s forwards';

            // Navigate after explosion animation completes
            setTimeout(function () {
                window.location.href = 'tutors.html';
            }, 500);
        }, 1500);
    });
}

function setupTutorsPage() {
    // Animate the tutor cards with a staggered teleport effect
    const tutorCards = document.querySelectorAll('.tutor-card');

    tutorCards.forEach((card, index) => {
        // Set a staggered delay for each card
        setTimeout(() => {
            card.style.animation = 'teleport 0.8s forwards';
        }, 300 * index);

        // Add hover effect
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = '0 15px 40px rgba(255, 204, 0, 0.5)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5)';
        });

        // Add click event to navigate to subject page (future functionality)
        card.addEventListener('click', () => {
            card.style.transform = 'scale(1.1)';
            setTimeout(() => {
                card.style.transform = 'scale(1)';
                alert(`You selected ${card.querySelector('h3').textContent}! Future functionality will take you to the subject page.`);
            }, 300);
        });
    });
}