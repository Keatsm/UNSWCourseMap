export default function Legend({ tailWindMap }) {
    return (
            <div className="absolute top-0 right-0 p-4">
                <h5>Course Fields</h5>
                <div className="flex flex-col space-y-1">
                    {Object.entries(tailWindMap).map(([key, value]) => (
                        <div className="flex items-center space-x-2">
                            <div style={{
                                backgroundColor: value
                            }} className={`w-4 h-4 rounded-full`} />
                            <span className="text-sm">{key}</span>
                        </div>
                    ))}
                </div>
            </div>
    )
}