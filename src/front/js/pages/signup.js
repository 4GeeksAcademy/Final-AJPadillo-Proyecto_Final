import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const Signup = () => {
    // Definimos los estados locales para el email y la contraseña
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    // Obtenemos el contexto global para acceder a las acciones
    const { store, actions } = useContext(Context);
    // Usamos navigate para redirigir después de un registro exitoso
    const navigate = useNavigate();
    // Esta función maneja el envío del formulario
    const handleSignup = async (e) => {
        e.preventDefault(); // Prevenimos la acción por defecto del formulario (recargar la página)
        // Llamamos a la función createUser del contexto global
        const userCreated = await actions.createUser(email, password);
        if (userCreated) {
            console.log("Usuario creado con éxito");
            navigate('/login'); // Redirigimos a la página de login
        } else {
            console.log("Fallo al crear el usuario");
        }
    };

    return (
        <div className="container">
            <p className="m-auto text-center display-1">Singup</p>
            <form onSubmit={handleSignup}>
                <div className="mb-3">
                    <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                    <input
                        type="email"
                        className="form-control"
                        id="exampleInputEmail1"
                        aria-describedby="emailHelp"
                        value={email} // El valor del input está vinculado al estado email
                        onChange={(e) => setEmail(e.target.value)} // Actualizamos el estado email al cambiar el input
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                    <input
                        type="password"
                        className="form-control"
                        id="exampleInputPassword1"
                        value={password} // El valor del input está vinculado al estado password
                        onChange={(e) => setPassword(e.target.value)} // Actualizamos el estado password al cambiar el input
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>
    );
};
