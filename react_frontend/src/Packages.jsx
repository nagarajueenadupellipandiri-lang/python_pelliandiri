
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import "./Packages.css";

const API_URL = "http://127.0.0.1:8000";

const COMMON_PAYLOAD = {
    type: "login",
    Authkey: "pppudanee",
};

function Packages() {
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [subcategories, setSubcategories] = useState([]);

    const [loadingCategories, setLoadingCategories] = useState(true);
    const [loadingSubcategories, setLoadingSubcategories] = useState(false);

    const [error, setError] = useState("");

    // --------------------------------
    // 1. Fetch Categories
    // --------------------------------
    const fetchCategories = async () => {
        try {
            setLoadingCategories(true);
            setError("");

            const response = await fetch(
                `${API_URL}/packages/categories`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        ...COMMON_PAYLOAD,
                        params: {},
                    }),
                }
            );

            const result = await response.json();

            if (!response.ok || !result.status) {
                throw new Error(
                    result.detail ||
                    result.message ||
                    "Unable to fetch categories"
                );
            }

            const categoryList = result.data || [];

            setCategories(categoryList);

            if (categoryList.length > 0) {
                setSelectedCategory(categoryList[0]);
            } else {
                setSelectedCategory(null);
            }

        } catch (error) {
            console.error("Category API Error:", error);
            setError(error.message || "Something went wrong");
        } finally {
            setLoadingCategories(false);
        }
    };


    // --------------------------------
    // 2. Fetch Category-wise Subcategories
    // --------------------------------
    const fetchSubcategories = async (categoryId) => {
        try {
            setLoadingSubcategories(true);
            setSubcategories([]);
            setError("");

            const response = await fetch(
                `${API_URL}/packages/frontend/subCategories`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        ...COMMON_PAYLOAD,
                        params: {
                            main_catid: categoryId,
                        },
                    }),
                }
            );

            const result = await response.json();

            if (!response.ok || !result.status) {
                throw new Error(
                    result.detail ||
                    result.message ||
                    "Unable to fetch subcategories"
                );
            }

            setSubcategories(result.data || []);

        } catch (error) {
            console.error("Subcategory API Error:", error);
            setSubcategories([]);
            setError(error.message || "Something went wrong");
        } finally {
            setLoadingSubcategories(false);
        }
    };


    // --------------------------------
    // 3. Load Categories on Page Open
    // --------------------------------
    useEffect(() => {
        fetchCategories();
    }, []);


    // --------------------------------
    // 4. Load Subcategories when Category Changes
    // --------------------------------
    useEffect(() => {
        if (selectedCategory) {
            fetchSubcategories(selectedCategory.id);
        } else {
            setSubcategories([]);
        }
    }, [selectedCategory]);


    // --------------------------------
    // 5. Category Selection
    // --------------------------------
    const handleCategoryChange = (category) => {
        setSelectedCategory(category);
    };


    // --------------------------------
    // 6. Complete Packages Page
    // --------------------------------
    return (
        <div className="website">

            {/* NAVBAR */}
            <Navbar />


            {/* PACKAGES CONTENT */}
            <main className="packages-page">

                <div className="packages-header">

                    <span className="packages-subtitle">
                        PELLIPANDIRI
                    </span>

                    <h1>Our Wedding Packages</h1>

                    <p>
                        Explore our exclusive wedding services and choose
                        the perfect package for your special day.
                    </p>

                </div>


                {loadingCategories ? (

                    <div className="packages-message">
                        Loading categories...
                    </div>

                ) : error && categories.length === 0 ? (

                    <div className="packages-error">
                        {error}
                    </div>

                ) : categories.length === 0 ? (

                    <div className="packages-message">
                        No Packages Available
                    </div>

                ) : (

                    <div className="packages-layout">

                        {/* LEFT SIDE - CATEGORIES */}
                        <section className="categories-panel">

                            <h2>Package Categories</h2>

                            <div className="category-list">

                                {categories.map((category) => (

                                    <button
                                        key={category.id}
                                        type="button"
                                        className={`category-item ${
                                            selectedCategory?.id === category.id
                                                ? "active"
                                                : ""
                                        }`}
                                        onClick={() =>
                                            handleCategoryChange(category)
                                        }
                                    >

                                        <span>
                                            {category.package_name}
                                        </span>

                                        <span className="category-arrow">
                                            ›
                                        </span>

                                    </button>

                                ))}

                            </div>

                        </section>


                        {/* RIGHT SIDE - SUBCATEGORIES */}
                        <section className="subcategories-panel">

                            <div className="subcategories-heading">

                                <div>

                                    <span className="packages-subtitle">
                                        EXPLORE SERVICES
                                    </span>

                                    <h2>
                                        {selectedCategory?.package_name || "Services"}
                                    </h2>

                                </div>

                            </div>


                            {loadingSubcategories ? (

                                <div className="packages-message">
                                    Loading services...
                                </div>

                            ) : error ? (

                                <div className="packages-error">
                                    {error}
                                </div>

                            ) : subcategories.length === 0 ? (

                                <div className="no-services">

                                    <div className="no-services-icon">
                                        ♡
                                    </div>

                                    <h3>No Services Available</h3>

                                    <p>
                                        There are currently no services available
                                        in this category.
                                    </p>

                                </div>

                            ) : (

                                <div className="subcategory-grid">

                                    {subcategories.map((subCategory) => (

                                        <article
                                            className="subcategory-card"
                                            key={subCategory.cid}
                                        >

                                            <div className="subcategory-icon">
                                                ♡
                                            </div>

                                            <h3>
                                                {subCategory.subcatname}
                                            </h3>

                                            <span className="subcategory-link">
                                                Explore Service →
                                            </span>

                                        </article>

                                    ))}

                                </div>

                            )}

                        </section>

                    </div>

                )}

            </main>


            {/* FOOTER */}
            <Footer />

        </div>
    );
}

export default Packages;
