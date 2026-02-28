export default function PrivacyPolicyPage() {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto bg-white p-8 sm:p-12 shadow rounded-lg">
                <h1 className="text-3xl font-extrabold text-gray-900 mb-8">Privacy Policy</h1>

                <div className="prose prose-indigo prose-lg text-gray-600">
                    <p className="leading-relaxed mb-6">Last updated: {new Date().toLocaleDateString()}</p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">1. Introduction</h2>
                    <p className="leading-relaxed mb-6">
                        Welcome to VTE (Verified Transaction Execution). We respect your privacy and are committed to protecting your personal data.
                        This privacy policy will inform you as to how we look after your personal data when you visit our website and tell you about your privacy rights.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">2. The Data We Collect About You</h2>
                    <p className="leading-relaxed mb-6">
                        We may collect, use, store and transfer different kinds of personal data about you which we have grouped together follows:
                    </p>
                    <ul className="list-disc pl-6 mb-6 space-y-2">
                        <li><strong>Identity Data</strong> includes first name, last name, username or similar identifier.</li>
                        <li><strong>Contact Data</strong> includes email address and telephone numbers.</li>
                        <li><strong>Technical Data</strong> includes internet protocol (IP) address, your login data, browser type and version.</li>
                        <li><strong>Usage Data</strong> includes information about how you use our application and services.</li>
                    </ul>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">3. How We Use Your Personal Data</h2>
                    <p className="leading-relaxed mb-6">
                        We will only use your personal data when the law allows us to. Most commonly, we will use your personal data in the following circumstances:
                    </p>
                    <ul className="list-disc pl-6 mb-6 space-y-2">
                        <li>Where we need to perform the contract we are about to enter into or have entered into with you.</li>
                        <li>Where it is necessary for our legitimate interests (or those of a third party) and your interests and fundamental rights do not override those interests.</li>
                        <li>Where we need to comply with a legal or regulatory obligation.</li>
                    </ul>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">4. Data Security</h2>
                    <p className="leading-relaxed mb-6">
                        We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorised way, altered or disclosed.
                        In addition, we limit access to your personal data to those employees, agents, contractors and other third parties who have a business need to know.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">5. Your Legal Rights</h2>
                    <p className="leading-relaxed mb-6">
                        Under certain circumstances, you have rights under data protection laws in relation to your personal data, including the right to request access, correction, erasure, restriction, transfer, to object to processing, to portability of data and (where the lawful ground of processing is consent) to withdraw consent.
                    </p>
                </div>
            </div>
        </div>
    );
}
