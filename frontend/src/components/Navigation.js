import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars } from '@fortawesome/free-solid-svg-icons'
import { useTransition, animated } from 'react-spring'
import NavigationMenu from "./NavigationMenu"

function Navigation() {
    const [showMenu, setShowMenu] = useState(false)

    const menuTransitions = useTransition(showMenu, null, {
        from: { transform: 'translateX(-100%)' },
        enter: { transform: 'translateX(0%)' },
        leave: { transform: 'translateX(-100%)' },
    })

    const overlayTransitions = useTransition(showMenu, null, {
        from: { opacity: 0 },
        enter: { opacity: 1 },
        leave: { opacity: 0 },
    })

    return (
        <nav>
            <FontAwesomeIcon
                className="fa-2x"
                icon={faBars}
                onClick={() => setShowMenu(!showMenu)}
            />
            {
                menuTransitions.map(({ item, props, key }) => item &&
                    <animated.div
                        key={key}
                        style={props}
                        id="menu">

                        <NavigationMenu
                            closeMenu = {
                                () => setShowMenu(false)
                            }
                        />

                    </animated.div>)
            }
            {
                overlayTransitions.map(({ item, props, key }) => item &&
                    <animated.div
                        key={key}
                        style={props}
                        className="overlay"
                        onClick={() => setShowMenu(false)}
                    >
                    </animated.div>)
            }
        </nav>
    );
}

export default Navigation;