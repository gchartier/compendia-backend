import React from 'react';
import { Link } from "react-router-dom";

function NavigationMenu(props) {
    return (
        <ul>
            <li>
                <Link
                    to="/"
                    onClick={props.closeMenu}
                >
                    Home
                </Link>
            </li>
            <li>
                <Link
                    to="/new-releases"
                    onClick={props.closeMenu}
                >
                    New Releases
                </Link>
            </li>
        </ul>
    );
}

export default NavigationMenu;